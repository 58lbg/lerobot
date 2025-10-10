import asyncio
import os
import uuid

import websockets
import ssl
import json


class WSServer:
    def __init__(self, message_callback=None):
        self.host = '10.253.104.55'
        # self.host = '10.253.58.135'
        self.port = 8084
        self.clients = {}
        self.clients_name = {}
        self.received_messages = []  # 用于存储接收到的消息

        # 创建 SSL 上下文以支持 WSS
        self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

        # 设置 certfile 和 keyfile 的路径为固定的相对路径
        certfile_path = os.path.join(os.path.dirname(__file__), './res/certificate.crt')
        keyfile_path = os.path.join(os.path.dirname(__file__), './res/private.key')

        self.ssl_context.load_cert_chain(certfile_path, keyfile_path)

        self.server = None
        self.server_task = None
        self.loop = None

        self.message_callback = message_callback if message_callback else self.receive_msg

    async def handler(self, websocket, path):
        # 新的客户端连接时，添加到 clients 集合
        client_name = str(uuid.uuid4())
        self.clients[client_name] = websocket
        try:
            # 发送 JSON 消息
            # message = {"type": "greeting", "content": "Hello, WebSocket client!"}
            async for message in websocket:
                # 当收到客户端消息时，存储消息
                # message = message.decode('utf-8', errors='replace')
                print(f"Received message: {message}")
                try:
                    if (client_name not in self.clients_name):
                        json_data = json.loads(message)
                        temp_get = str(json_data.get("clientName", None))
                        if temp_get and len(temp_get) > 0:
                            self.clients_name[client_name] = temp_get
                            await self.send_message({
                                "text": "hello client 你好 客户端",
                                "clientName": temp_get
                            })
                            print(self.clients_name)
                except Exception as e:
                    print(str(e))
                if self.message_callback:
                    await self.message_callback(message)
                else:
                    self.received_messages.append(message)
        except websockets.ConnectionClosed as e:
            print("Client disconnected：" + e.code + "  " + e.reason)
        finally:
            # 移除已断开连接的客户端
            self.clients.pop(client_name, None)
            self.clients_name.pop(client_name, None)
            print(self.clients_name)

    async def receive_msg(self, msg):
        print(f"func receive_msg: {msg}")

    async def send_message(self, message: dict):
        # 将字典序列化为 JSON 字符串
        json_message = json.dumps(message, ensure_ascii=False)
        print(f"send msg: {json_message}")
        # json_message = json_message.encode('utf-8', errors='ignore')
        # 向所有已连接的客户端广播消息
        if self.clients:
            # 使用 asyncio.gather 来并发运行协程
            client_name = message.get("clientName")
            if client_name and client_name in self.clients_name.values():
                targets = [self.clients[k] for k, v in self.clients_name.items() if v == client_name]
                await asyncio.gather(*[c.send(json_message) for c in targets])
            else:
                await asyncio.gather(*[client.send(json_message) for client in self.clients.values()])

    def send_message_no_wait(self, message: dict):
        asyncio.create_task(self.send_message(message))

    async def get_message(self):
        # 获取收到的最新消息（如果有）
        if self.received_messages:
            return self.received_messages.pop(0)  # 先进先出
        else:
            return None

    async def _start_server(self):
        # 启动 WebSocket 服务器
        print(f"WebSocket server started on {self.host}:{self.port} with SSL")
        self.server = await websockets.serve(self.handler, self.host, self.port,ping_interval=10,   # 每 20 秒自动发 ping
                                    ping_timeout=5, ssl=self.ssl_context)

    def startByAi(self):
        print(f"start car server")
        self.loop = asyncio.get_event_loop()
        # 使用 asyncio.run() 启动事件循环
        self.server_task = asyncio.create_task(self._start_server())

    async def _stop(self):
        for key, socket in self.clients.items():
            await socket.close()
        self.clients.clear()
        self.clients_name.clear()
        if self.server:
            self.server.close()
            await (self.server.wait_closed())
        if self.server_task:
            self.server_task.cancel()
        # if self.loop:
        #     self.loop.stop()
        print(f"ros car wss close")

    def stop(self):
        asyncio.create_task(self._stop())

    def start(self):
        # 启动 WebSocket 服务器
        self.loop = asyncio.get_event_loop()
        self.server = websockets.serve(self.handler, self.host, self.port, ssl=self.ssl_context)
        self.loop.run_until_complete(self.server)
        print(f"WebSocket server started on {self.host}:{self.port} with SSL")

        self.loop.run_forever()


# 创建并启动 WSS 服务
if __name__ == "__main__":
    server = WSServer()
    server.start()
