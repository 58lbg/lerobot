#!/usr/bin/env python
# encoding: utf-8
import os

import rospy
import ssl
import websocket
import subprocess
import json
import time  # 用于休眠等待
from go_bot import GoBot
from std_msgs.msg import Float32
from ros_audio_play import AudioPlayer, get_audio_file

import sys
IS_PY2 = sys.version_info[0] == 2


class WSClient:

    def __init__(self):
        self.uri = "wss://10.253.104.55:8084"  # WebSocket 服务器 URI
        # self.uri = "wss://roscarlivestream.58.com/rccar"  # WebSocket 服务器 URI
        self.ws = None
        self.move_bot = GoBot()
        self.reconnect_attempts = 0  # 重连次数
        self.max_reconnect_attempts = 5  # 最大重连次数
        self.reconnect_delay = 5  # 重连延迟时间（秒）
        self.voltage = 0
        self.executed = False
        self.ros_audio_play = AudioPlayer()
        self.client_name = "car"
        rospy.Subscriber('/PowerVoltage', Float32, self.voltage_callback)

    def voltage_callback(self, msg):
        # rospy.loginfo("电池电压:{}".format(msg))
        self.voltage = msg
        if msg < 10.3:
            time.sleep(5)  # 延迟 5 秒
            if not self.executed:
                # 使用新的音频文件路径
                audio_file = get_audio_file()
                self.ros_audio_play.play_audio(audio_file, play_count=3)
                self.move_bot.multi_point_navigation(["vase"])
                self.executed = True

    def on_message(self, ws, message):
        print("Received message: %s" % message)
        dict_data = json.loads(message)
        print("dict_data: %s" % dict_data)
        # 收到消息后执行脚本
        if self.voltage > 10.3:
            self.execute_script(dict_data)

    def send_message(self, message):
        if self.ws:
            message["clientName"] = self.client_name
            print("Send message: {}".format(message))
            msg = json.dumps(message, ensure_ascii=False)
            self.ws.send(msg)

    def on_error(self, ws, error):
        print("Error: %s" % error)
        self.ws = None
        self.reconnect()

    def on_close(self, ws, close_status_code, close_msg):
        self.ws = None
        print("### WebSocket closed ###")
        print("Close status: %d, message: %s" % (close_status_code, close_msg))
        self.reconnect()

    def on_open(self, ws):
        print("Connected Success")
        print("Connected to %s" % self.uri)
        # 在连接打开时可以发送消息
        ws.send("Hello, Server")
        # 重置重连次数
        self.reconnect_attempts = 0
        # json_data = '{"target": "\\u6d17\\u8863\\u533a", "cmd": "object", "distant": "0", "message": null, "type": "operator", "deg": "0"}'
        # dict_data = json.loads(json_data)
        # self.execute_script(dict_data)

    def execute_script(self, message):
        try:
            print("dict_data: %s" % type(message))
            # 使用 subprocess.call 执行外部脚本
            if IS_PY2 :
                if u'cmd' in message and u'target' in message:
                    cmd = message[u"cmd"]
                    target = message[u"target"]
                    print("cmd:" + cmd)
                    cmd = message[u"cmd"]
                    target = message[u"target"].encode('utf8')  # 转换为 Unicode
                    distant = message[u"distant"].encode('utf8')
                    deg = message[u"deg"].encode('utf8')
                    self.move_bot.execute_action(cmd, target, distant, deg)
            else:
                if 'cmd' in message and 'target' in message:
                    cmd = message["cmd"]
                    target = message["target"]
                    print("cmd:" + cmd)
                    cmd = message["cmd"]
                    target = message["target"]  # 转换为 Unicode
                    distant = message["distant"]
                    deg = message["deg"]
                    self.move_bot.execute_action(cmd, target, distant, deg)

            # else:
            #     print ("没有cmd字段 或者 没有target字段")

        except Exception as e:
            print("Failed to execute script: %s" % e)

    def reconnect(self):
        # 判断是否已经超过最大重连次数
        print("开始从新链接。。。。")
        if self.reconnect_attempts < self.max_reconnect_attempts:
            self.reconnect_attempts += 1
            time.sleep(self.reconnect_delay)  # 等待一定时间再重连
            self.connect()  # 重新连接
        else:
            print("Max reconnect attempts reached. Giving up.")

    def connect(self):
        try:
            headers = {"Authorization": "9vw%TqPvGFxd0Heu0AAYXV3l4RRPHyvEiP=TS9yaJgdkHtTO"}
            # 创建 WebSocket 客户端
            self.ws = websocket.WebSocketApp(self.uri,
                                             header=headers,
                                             on_message=self.on_message,
                                             on_error=self.on_error,
                                             on_close=self.on_close,
                                             on_open=self.on_open)
            # 忽略 SSL 证书验证（适用于测试环境）
            self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE}, ping_interval=10, ping_timeout=5)

        except Exception as e:
            print("Error during connection: %s" % e)
            self.reconnect()


# 创建并启动 WebSocket 客户端
if __name__ == "__main__":
    rospy.init_node("wss_client")
rospy.loginfo("启动 wss_client 节点 ")
client = WSClient()
client.connect()
rospy.spin()
