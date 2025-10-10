import asyncio
import websockets
import json
import logging
import time
from dataclasses import asdict
from pprint import pformat
from typing import Dict, Optional

import numpy as np
import torch
from lerobot.common.robot_devices.motors.feetech import FeetechMotorsBus, TorqueMode
from lerobot.common.robot_devices.robots.manipulator import ensure_safe_goal_position
from lerobot.common.robot_devices.robots.mobile_manipulator import MobileManipulator
from lerobot.common.robot_devices.utils import busy_wait, safe_disconnect
from lerobot.common.utils.utils import init_logging
from lerobot.configs import parser
from lerobot.common.robot_devices.robots.utils import Robot, make_robot_from_config
from lerobot.common.robot_devices.control_configs import ControlPipelineConfig

# 初始化日志
init_logging()

from ikpy.chain import Chain
from ikpy.link import URDFLink, OriginLink
import numpy as np

so100_chain = Chain.from_urdf_file("/Users/wangyoukun/Desktop/lerobot/config/so_arm100.urdf", base_elements=["Base"])
class PhoneControlRobot:
    def __init__(self, robot_config: ControlPipelineConfig):
        # 初始化机器人
        self.robot = make_robot_from_config(robot_config)
        self.robot_config = robot_config
        self.robot.connect()
        
        # 获取电机总线
        self.motors_bus = self.robot.follower_arms["main"]

        # 初始化上一次的位置和旋转
        self.last_position = None
        self.last_rotation = None
        
        # 从配置中获取控制参数
        self.control_fps = self.robot_config.control.fps if hasattr(self.robot_config, 'control') else 30
        self.max_relative_target = self.robot_config.max_relative_target 
        # # 从配置中获取夹爪参数
        # if hasattr(self.robot.config, 'follower_arms') and 'main' in self.robot.config.follower_arms:
        #     gripper_config = self.robot.config.follower_arms['main'].motors.get('gripper', {})
        #     self.gripper_closed_pos = gripper_config.get('closed_position', 0)
        #     self.gripper_open_pos = gripper_config.get('open_position', 100)
        # else:
        self.gripper_closed_pos = 0
        self.gripper_open_pos = 100
        
            
    def _get_relative_movement(self, current_pos: Dict, current_rot: Dict) -> tuple:
        """计算相对运动"""
        if self.last_position is None or self.last_rotation is None:
            # 第一次运动，直接返回当前位置
            return current_pos, current_rot
            
        # 计算相对位置
        relative_pos = {
            'x': current_pos['x'] - self.last_position['x'],
            'y': current_pos['y'] - self.last_position['y'],
            'z': current_pos['z'] - self.last_position['z']
        }
        
        # 计算相对旋转
        relative_rot = {
            'roll': current_rot['roll'] - self.last_rotation['roll'],
            'pitch': current_rot['pitch'] - self.last_rotation['pitch'],
            'yaw': current_rot['yaw'] - self.last_rotation['yaw']
        }
        
        return relative_pos, relative_rot
            
    def process_pose_data(self, data):
        """处理接收到的姿态数据"""
        try:
            if data['type'] == 'pose':
                start_loop_t = time.perf_counter()
                
                # 获取位置和旋转信息
                position = data['position']
                rotation = data['rotation']
                gripper_state = data['gripper']
                
                # 计算相对运动
                # relative_pos, relative_rot = self._get_relative_movement(position, rotation)
                
                # 更新上一次的位置和旋转
                self.last_position = position
                self.last_rotation = rotation
                
                # 从配置中获取机械臂电机名称
                arm_motor_names = []
                for motor_name in self.motors_bus.motor_names:
                    if motor_name not in ["gripper"]:
                        arm_motor_names.append(motor_name)
                
                # 获取当前电机位置
                current_angles = self.motors_bus.read("Present_Position", arm_motor_names)
                
                # 将相对运动转换为电机运动数据
                joint_angles:np = so100_chain.inverse_kinematics([position['x'],position['y'],position['z']],[rotation['roll'],rotation['pitch'],rotation['yaw']],"Y")
                
                # 获取当前夹爪位置
                current_gripper_pos = self.motors_bus.read("Present_Position", "gripper")
                # current_gripper_pos = torch.tensor([current_gripper_pos])
                # 计算夹爪目标位置，给所有值加上 0.5
                gripper_target_pos = current_gripper_pos + 0.5

                # 计算新的目标位置（当前位置 + 相对运动）
                target_angles = current_angles + joint_angles
                
                
                # 构建动作数据，包含机械臂和夹爪
                action = np.concatenate([target_angles, gripper_target_pos])

            
                goal_pos = torch.tensor(action)
                
                # # 发送动作到从动臂
                
                # 控制帧率
                dt_s = time.perf_counter() - start_loop_t
                busy_wait(1 / self.control_fps - dt_s)
                
                # 记录控制信息
                dt_s = time.perf_counter() - start_loop_t
                logging.info(f"控制周期: {dt_s:.3f}s")
           
                present_pos = self.motors_bus.read("Present_Position")
                present_pos = torch.from_numpy(present_pos)
                goal_pos = ensure_safe_goal_position(goal_pos, present_pos, 0.5)



                goal_pos = goal_pos.numpy().astype(np.float32)
                self.motors_bus.write("Goal_Position", goal_pos)
                
        except Exception as e:
            logging.error(f"处理姿态数据时出错: {e}")
            
    def stop(self):
        """停止所有电机"""
        if self.robot.is_connected:
            self.robot.disconnect()

class RobotWebSocketHandler:
    def __init__(self, robot):
        self.robot = robot
    
    async def handle_message(self, websocket):
        async for message in websocket:
            try:
                data = json.loads(message)
                # 使用robot处理姿态数据
                self.robot.process_pose_data(data)
            except json.JSONDecodeError as e:
                print("解析失败:", e)

async def main(robot_config):
    """主函数"""
    try:
        # 创建机器人实例
        robot = PhoneControlRobot(robot_config)
        
        # 创建处理器实例
        handler = RobotWebSocketHandler(robot)
        
        # 启动 WebSocket 服务器
        async with websockets.serve(handler.handle_message, "0.0.0.0", 8080):
            print("WebSocket 服务器启动，监听 8080 端口...")
            await asyncio.Future()  # 永不返回，保持运行状态

            
    except Exception as e:
        logging.error(f"程序运行出错: {e}")
    finally:
        # 确保机器人正确停止
        robot.stop()

@parser.wrap()
def control_robot_with_phone(cfg: ControlPipelineConfig):
    """通过手机控制机器人的主函数"""
    logging.info(pformat(asdict(cfg)))
    asyncio.run(main(cfg.robot))

if __name__ == "__main__":
    control_robot_with_phone()