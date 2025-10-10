import json
import subprocess

from config.wss.ros_car_wss import WSServer
from config.lift.lift_control import run_lift
import asyncio

class MessageProcessor:
    def __init__(self):
        """
        :param handler: 消息处理函数，接收 str
        """
        self.queue: asyncio.Queue[str] = asyncio.Queue()
        self.running = False
        self.server: WSServer | None = None
        self.clients = []
        self.run_task = False

        self.task_list = [
                {
                    "type": "send",
                    "continue": False,
                    "content":
                        {
                            "clientName": "car",
                            "cmd": "object",
                            "target": "shelf",
                            "distant": 0,
                            "deg": 0,
                        }
                },
                {
                    "type": "wait",
                    "content":
                        {
                            "clientName": "car",
                            "type": "carStatus",
                            "target":"shelf",
                            "status":3
                        },
                    "continue": True,
                },
                # {
                #     "type": "lift",
                #     "cycle": 120,
                #     "continue": True,
                # },
                {
                    "type": "send",
                    "continue": False,
                    "content":
                        {
                            "clientName": "car",
                            "cmd": "move",
                            "target": "None",
                            "distant": 0.50,
                            "deg": 0,
                        }
                },
                {
                    "type": "wait",
                    "content":
                        {
                            "clientName": "car",
                            "type": "carStatus",
                            "target": "move_action",
                            "status": 3
                        },
                    "continue": True,
                },
                {
                    "type": "send",
                    "continue": True,
                    "content":
                        {
                            "clientName": "client_55",
                            "cmd": "eval",
                            "sleep": 15,
                            "target": "grap",
                        }
                },
                {
                    "type": "shell",
                    "continue": True,
                    "script": "./config/lekiwi_car/start_host.sh",
                    "exitCode": 100,
                },

                # {
                #     "type": "lift",
                #     "cycle": -120,
                #     "continue": True,
                # },
                {
                    "type": "send",
                    "continue": False,
                    "content":
                        {
                            "clientName": "car",
                            "cmd": "object",
                            "target": "release2",
                            "distant": 0,
                            "deg": 0,
                        }
                },
                {
                    "type": "wait",
                    "content":
                        {
                            "clientName": "car",
                            "type": "carStatus",
                            "target": "release2",
                            "status": 3
                        },
                    "continue": True,
                },
                {
                    "type": "send",
                    "continue": False,
                    "content":
                        {
                            "clientName": "car",
                            "cmd": "move",
                            "target": "None",
                            "distant": 0.35,
                            "deg": 0,
                        }
                },
                {
                    "type": "wait",
                    "content":
                        {
                            "clientName": "car",
                            "type": "carStatus",
                            "target": "move_action",
                            "status": 3
                        },
                    "continue": True,
                },
                {
                    "type": "send",
                    "continue": True,
                    "content":
                        {
                            "clientName": "client_55",
                            "cmd": "eval",
                            "sleep": 15,
                            "target": "release",
                        }
                },
                {
                    "type": "shell",
                    "continue": True,
                    "script": "./config/lekiwi_car/start_host.sh",
                    "exitCode": 100,
                },
                {
                    "type": "send",
                    "continue": False,
                    "content":
                        {
                            "clientName": "car",
                            "cmd": "object",
                            "target": "home",
                            "distant": 0,
                            "deg": 0,
                        }
                },
                {
                    "type": "wait",
                    "content":
                        {
                            "clientName": "car",
                            "type": "carStatus",
                            "target": "home",
                            "status": 3
                        },
                    "continue": True,
                },
            ]


    async def start(self, server: WSServer):
        """循环读取队列并同步处理"""
        self.server = server
        self.running = True
        while self.running:
            message = await self.queue.get()  # 阻塞直到有消息
            try:
                await self.handle_msg(message)
            except Exception as e:
                print("处理消息异常:", e)

    async def handle_msg(self, msg: str):
        print("处理消息:", msg)
        json_data = json.loads(msg)
        name = json_data.get("clientName", None)
        if name and name not in self.clients:
            self.clients.append(name)
            self.check_clients()
        if self.run_task:
            await self.execute_task(json_data)

    async def execute_task(self, json_data: dict):
        if len(self.task_list) == 0:
            print("任务完成，结束")
            self.stop()
            return
        task = self.task_list[0]
        is_execute = False
        if task["type"] == "send":
            await self.server.send_message(task["content"])
            is_execute = True
        elif task["type"] == "wait":
            is_ok = True
            for key, value in task["content"].items():
                if key not in json_data.keys() or value != json_data[key]:
                    is_ok = False
                    break
            if is_ok:
                is_execute = True
        elif task["type"] == "lift":
            run_lift(task["cycle"])
            is_execute = True
        elif task["type"] == "shell":
            # 执行脚本
            result = subprocess.run(["bash", task.get("script", None)])
            # 打印退出码
            print("退出码:", result.returncode)
            if result.returncode == task["exitCode"]:
                is_execute = True
            else:
                self.running = False
                print("执行抓取失败")
                return
        if is_execute:
            self.task_list.pop(0)
            if task.get("continue", False):
                await self.execute_task(json_data)

    def check_clients(self):
        if "car" in self.clients and "client_55" in self.clients:
            self.run_task = True

    def stop(self):
        """停止循环"""
        self.running = False
        self.server.stop()

    async def receive_msg(self, message: str):
        """server 回调时调用，将消息放入队列"""
        await self.queue.put(message)


if __name__ == "__main__":
    messageProcessor = MessageProcessor()
    run_server = WSServer(messageProcessor.receive_msg)
    loop = asyncio.get_event_loop()
    # 把 messageProcessor.start() 放到同一个事件循环
    loop.create_task(messageProcessor.start(run_server))
    run_server.start()
