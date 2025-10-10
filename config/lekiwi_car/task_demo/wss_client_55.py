import asyncio
import json
import subprocess
import time

from config.wss.ros_car_wss_client import WSClient
async def msg_receive(msg:str):
    print("client_55 receive msg : " + msg)
    json_data = json.loads(msg)
    time = json_data.get("sleep", 1)
    if time > 1:
        await asyncio.sleep(time)
    if json_data.get("target", None) == "grap":
        subprocess.Popen(
            ["bash", './config/eval.sh'],
            close_fds=True,
            start_new_session=True  # 关键，子进程脱离当前进程组
        )
    elif json_data.get("target", None) == "release":
        subprocess.Popen(
            ["bash", './config/eval.sh', "release"],
            close_fds=True,
            start_new_session=True  # 关键，子进程脱离当前进程组
        )
    print("msg_receive end")

if __name__ == "__main__":
    client = WSClient("client_55", msg_receive)
    client.start()
