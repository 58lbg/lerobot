import asyncio
import inspect
import json
import sys

import websockets
import ssl

class WSClient:
    def __init__(self, client_name="car", msg_callback=None):
        self.uri = "wss://10.253.104.55:8084"
        # self.uri = "wss://10.253.58.135:8084"
        self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        self.client_name = client_name
        self.msg_callback = msg_callback

    async def connect(self):
        async with websockets.connect(self.uri, ssl=self.ssl_context, ping_interval=10, ping_timeout=5) as websocket:
            self.websocket = websocket
            print(f"conneted {self.uri}")
            msg = json.dumps({"text":"你好 服务端"}, ensure_ascii=False)
            await self.send_message({"text":"你好 服务端"})
            await self.receive_messages()

    async def send_message(self, message: dict):
        if self.websocket:
            message["clientName"] = self.client_name
            print(f"Send message: {message}")
            msg = json.dumps(message, ensure_ascii=False)
            await self.websocket.send(msg)

    async def receive_messages(self):
        try:
            async for message in self.websocket:
                #message = message.decode('utf-8', errors='replace')
                print(f"Received message: {message}")
                if self.msg_callback:
                    # 异步执行，不阻塞 receive_messages 循环
                    if inspect.iscoroutinefunction(self.msg_callback):
                        task = asyncio.create_task(self.msg_callback(message))
                    else:
                        # 如果是同步函数，也放到线程池异步执行
                        loop = asyncio.get_running_loop()
                        loop.run_in_executor(None, self.msg_callback, message)
        except websockets.ConnectionClosed as e:
            print(f"Connection closed with code: {e.code} and reason: {e.reason}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def start(self):
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(self.connect())
        asyncio.run(self.connect())

# 创建并启动 WebSocket 客户端
if __name__ == "__main__":
    client = "car"
    if len(sys.argv) > 1:
        client = sys.argv[1]
    client = WSClient(client)
    client.start()