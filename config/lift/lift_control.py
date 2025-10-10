#!/usr/bin/env python3
# coding=utf-8
import time
import os
from scservo_sdk import protocol_packet_handler, port_handler, scservo_def

# =================== 配置 ===================
# 替换为实际端口
PORT_NAME = "/dev/ttyACM0"
BAUDRATE = 1000000
SERVO_ID = 10                # 电机ID
CIRCLE_FILE = "~/.cache/lerobot/current_circle.txt"
SPEED_MAX = 20000           # 最大速度
# SPEED_MAX = 50           # 最大速度
READ_INTERVAL = 1.25/4.0         # 秒，读取位置间隔
POSITION_MAX = 4097
PER_ADD_POS = 4097/4.0
MIDDLE_POS = 2000
PER_OFFSET = 200
MAX_CYCLE = 110
MIN_CYCLE = 0

# 地址定义
ADDR_MODE = 0x21            # 33
ADDR_POS = 0x38             # 56
ADDR_SPEED = 0x2E           # 46
CURRENT_SPEED = 0x3A        # 58



# ============================================

class CircleMotor:
    def __init__(self, port_name, baudrate, servo_id):
        self.port = port_handler.PortHandler(port_name)
        self.ph = protocol_packet_handler()
        self.servo_id = servo_id
        self.current_circle = 0
        self.prev_position = 0
        self.isRun = False
        self.cycle_path = os.path.expanduser(CIRCLE_FILE)
        self.load_circle()

    def open_port(self):
        if not self.port.openPort():
            raise RuntimeError("Failed to open port")
        self.port.setBaudRate(BAUDRATE)

    def close_port(self):
        self.port.closePort()

    def load_circle(self):
        if os.path.exists(self.cycle_path):
            try:
                with open(self.cycle_path, "r") as f:
                    self.current_circle = int(f.read().strip())
            except Exception as e:
                self.current_circle = 0
        else:
            self.current_circle = 0

    def save_circle(self):
        with open(self.cycle_path, "w") as f:
            f.write(str(self.current_circle))

    def set_speed_mode(self, speed):
        # 设置运行模式为恒速模式
        self.ph.write1ByteTxRx(self.port, self.servo_id, ADDR_MODE, 1)
        # 设置速度，正负号决定旋转方向
        self.ph.write2ByteTxRx(self.port, self.servo_id, ADDR_SPEED, speed)

        self.isRun = speed != 0

    def read_position(self):
        data, _, _ = self.ph.read2ByteTxRx(self.port, self.servo_id, ADDR_POS)
        return data

    def read_speed(self):
        data, _, _ = self.ph.read2ByteTxRx(self.port, self.servo_id, CURRENT_SPEED)
        return data

    def stop(self):
        if self.isRun:
            self.isRun = False

    def calculate_deviation(self, current_pos, target_pos, max_position=POSITION_MAX):
        """
        计算两个位置之间的实际偏差（考虑0-4096循环）

        参数:
            current_pos: 电机当前实际位置
            target_pos: 预测的目标位置
            max_position: 最大位置值（4096）

        返回:
            最小偏差绝对值
        """
        # 计算正向和反向偏差
        diff1 = (target_pos - current_pos) % max_position
        diff2 = (current_pos - target_pos) % max_position

        # 返回最小的偏差（考虑循环的情况）
        return min(diff1, diff2)

    def run_circle(self, target_circle):
        if target_circle + self.current_circle >= MAX_CYCLE:
            target_circle = MAX_CYCLE - self.current_circle
        elif target_circle + self.current_circle <= MIN_CYCLE:
            target_circle = MIN_CYCLE - self.current_circle

        if target_circle == 0:
            return

        # 读取当前位置作为初始参考
        self.prev_position = self.read_position()

        # 设定速度方向
        speed = SPEED_MAX if target_circle > 0 else -SPEED_MAX
        self.set_speed_mode(speed)
        per_add_pos = PER_ADD_POS if target_circle > 0 else -PER_ADD_POS

        circles_to_go = abs(target_circle)
        completed = 0

        cycle_i = 0

        start = True
        last = False

        try:
            while completed < circles_to_go:
                if not self.isRun:
                    break
                if start:
                    time.sleep(READ_INTERVAL + 0.115)
                    start = False
                elif last:
                    time.sleep(READ_INTERVAL - 0.118)
                else:
                    time.sleep(READ_INTERVAL)
                cycle_i += 1
                if completed == circles_to_go - 1 and cycle_i == 3:
                    last = True
                current_pos = self.read_position()
                next_pos = (self.prev_position + per_add_pos) % POSITION_MAX
                diff = self.calculate_deviation(current_pos, next_pos)

                print(f"电机状态: {current_pos}  {self.prev_position} {next_pos} {diff}")
                # # 判断转过一圈
                # if abs(diff) < PER_OFFSET or (last and cycle_i == 4):
                #     if cycle_i % 4 == 0:
                #         if speed > 0:
                #             self.current_circle += 1
                #             completed += 1
                #         else:
                #             self.current_circle -= 1
                #             completed += 1
                #         cycle_i = 0
                #         # self.save_circle()
                #         print(f"完成 {completed} 圈，总圈数: {self.current_circle}")
                #     self.prev_position = current_pos

                # 判断转过一圈
                if abs(diff) < PER_OFFSET:
                    if speed > 0 and (self.prev_position < MIDDLE_POS <= current_pos):
                        self.current_circle += 1
                        completed += 1
                        print(f"完成 {completed} 圈，总圈数: {self.current_circle}")
                        self.save_circle()
                        if self.current_circle >= MAX_CYCLE:
                            print(f"已经到达顶端")
                            break
                    elif speed < 0 and current_pos < MIDDLE_POS <= self.prev_position:
                        self.current_circle -= 1
                        completed += 1
                        print(f"完成 {completed} 圈，总圈数: {self.current_circle}")
                        self.save_circle()
                        if self.current_circle <= MIN_CYCLE:
                            print(f"已经到达底端")
                            break
                    self.prev_position = current_pos
                else:
                    print(f"电机异常: {diff}")
                    break
        finally:
            # 停止电机
            self.set_speed_mode(0)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="ST3215 圈数控制")
    parser.add_argument("circle", type=int, help="旋转圈数，可为负")
    args = parser.parse_args()

    run_lift(args.circle)
    print("运行结束")
def run_lift(times):
    motor = CircleMotor(PORT_NAME, BAUDRATE, SERVO_ID)
    motor.open_port()
    motor.run_circle(times)
    motor.close_port()


if __name__ == "__main__":
    main()