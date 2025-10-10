import asyncio
import websockets
import json
import logging
import time
import pybullet as p
import pybullet_data
import numpy as np
from ikpy.chain import Chain

# === 加载 ikpy 模型 ===
so100_chain = Chain.from_urdf_file("/Users/wangyoukun/Desktop/lerobot/config/so_arm100.urdf", base_elements=["Base"])

# === 初始化 pybullet 模拟器 ===
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)
p.loadURDF("plane.urdf")
robot_id = p.loadURDF("/Users/wangyoukun/Desktop/lerobot/config/so_arm100.urdf", [0, 0, 0], useFixedBase=True)

joint_num = p.getNumJoints(robot_id)
joint_indices = [i for i in range(joint_num)]

# === 全局变量 ===
latest_pose_data = None
last_update_time = time.time()

def set_joint_positions(joint_angles):
    for i, angle in enumerate(joint_angles):
        if i < joint_num:
            p.setJointMotorControl2(
                bodyIndex=robot_id,
                jointIndex=joint_indices[i],
                controlMode=p.POSITION_CONTROL,
                targetPosition=angle,
                force=500
            )

async def robot_motion_loop():
    global latest_pose_data
    while True:
        now = time.time()
        if latest_pose_data and now - last_update_time < 1.0:
            try:
                data = latest_pose_data
                latest_pose_data = None  # 清除已处理的数据
                position = data['position']
                rotation = data['rotation']
                target_pos = [position['x'], position['y'], position['z']]
                # IK 解算（只用位置）
                joint_angles = so100_chain.inverse_kinematics(target_pos)
                set_joint_positions(joint_angles)
            except Exception as e:
                logging.error(f"IK或控制失败: {e}")
        p.stepSimulation()
        await asyncio.sleep(0.02)  # 控制频率 50Hz

def process_pose_data(data):
    global latest_pose_data, last_update_time
    if data['type'] == 'pose':
        latest_pose_data = data
        last_update_time = time.time()

async def handle_message(websocket):
    async for message in websocket:
        try:
            data = json.loads(message)
            process_pose_data(data)
        except json.JSONDecodeError as e:
            print("解析失败:", e)

async def main():
    try:
        asyncio.create_task(robot_motion_loop())
        async with websockets.serve(handle_message, "0.0.0.0", 8080):
            print("WebSocket 服务器启动，监听 8080 端口...")
            await asyncio.Future()
    except Exception as e:
        logging.error(f"程序运行出错: {e}")
    finally:
        p.disconnect()

def control_robot_with_phone():
    asyncio.run(main())

if __name__ == "__main__":
    control_robot_with_phone()