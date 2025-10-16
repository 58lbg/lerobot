# !/usr/bin/env python
import copy
import math
# Copyright 2025 The HuggingFace Inc. team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specif

import time
from pathlib import Path

import numpy as np

from lerobot.model.kinematics import RobotKinematics
from lerobot.processor import RobotAction, RobotObservation, RobotProcessorPipeline
from lerobot.processor.converters import (
    robot_action_observation_to_transition,
    transition_to_robot_action,
)
from lerobot.robots.so100_follower.config_so100_follower import SO100FollowerConfig
from lerobot.robots.so100_follower.robot_kinematic_processor import (
    EEBoundsAndSafety,
    EEReferenceAndDelta,
    GripperVelocityToJoint,
    InverseKinematicsEEToJoints,
)
from lerobot.robots.so100_follower.so100_follower import SO100Follower
from lerobot.teleoperators.phone.config_phone import PhoneConfig, PhoneOS
from lerobot.teleoperators.phone.phone_processor import MapPhoneActionToRobotAction
from lerobot.teleoperators.phone.teleop_phone import Phone
from lerobot.utils.robot_utils import busy_wait
from lerobot.utils.visualization_utils import init_rerun, log_rerun_data

def quaternion_to_euler(rot_cal):
    """
    将四元组 (w, x, y, z) 转换为欧拉角 (x, y, z)，单位为度
    对应 roll(x)、pitch(y)、yaw(z)
    """
    w, x, y, z = rot_cal

    # 计算 roll (x轴旋转)
    sinr_cosp = 2 * (w * x + y * z)
    cosr_cosp = 1 - 2 * (x * x + y * y)
    roll = math.atan2(sinr_cosp, cosr_cosp)

    # 计算 pitch (y轴旋转)
    sinp = 2 * (w * y - z * x)
    if abs(sinp) >= 1:
        pitch = math.copysign(math.pi / 2, sinp)  # 处理超范围情况
    else:
        pitch = math.asin(sinp)

    # 计算 yaw (z轴旋转)
    siny_cosp = 2 * (w * z + x * y)
    cosy_cosp = 1 - 2 * (y * y + z * z)
    yaw = math.atan2(siny_cosp, cosy_cosp)

    # 转换为角度
    roll_deg = math.degrees(roll)
    pitch_deg = math.degrees(pitch)
    yaw_deg = math.degrees(yaw)

    return roll_deg, pitch_deg, yaw_deg

FPS = 30

# Initialize the robot and teleoperator
robot_config = SO100FollowerConfig(
    port="/dev/ttyACM0",
    id="so100_follower",
    use_degrees=True,
    calibration_dir=Path(".cache/calibration/phone_teleop")
)
teleop_config = PhoneConfig(phone_os=PhoneOS.IOS)  # or PhoneOS.ANDROID

# Initialize the robot and teleoperator
robot = SO100Follower(robot_config)
teleop_device = Phone(teleop_config)

# NOTE: It is highly recommended to use the urdf in the SO-ARM100 repo: https://github.com/TheRobotStudio/SO-ARM100/blob/main/Simulation/SO101/so101_new_calib.urdf
kinematics_solver = RobotKinematics(
    urdf_path="./config/simulation/SO101/so101_new_calib.urdf",
    target_frame_name="gripper_frame_link",
    joint_names=list(robot.bus.motors.keys()),
)

# Build pipeline to convert phone action to ee pose action to joint action
phone_to_robot_joints_processor = RobotProcessorPipeline[tuple[RobotAction, RobotObservation], RobotAction](
    steps=[
        MapPhoneActionToRobotAction(platform=teleop_config.phone_os),
        EEReferenceAndDelta(
            kinematics=kinematics_solver,
            end_effector_step_sizes={"x": 0.5, "y": 0.5, "z": 0.5},
            motor_names=list(robot.bus.motors.keys()),
            use_latched_reference=True,
        ),
        EEBoundsAndSafety(
            end_effector_bounds={"min": [-1.0, -1.0, -1.0], "max": [1.0, 1.0, 1.0]},
            max_ee_step_m=0.10,
        ),
        GripperVelocityToJoint(
            speed_factor=20.0,
        ),
        InverseKinematicsEEToJoints(
            kinematics=kinematics_solver,
            motor_names=list(robot.bus.motors.keys()),
            initial_guess_current_joints=True,
        ),
    ],
    to_transition=robot_action_observation_to_transition,
    to_output=transition_to_robot_action,
)

# Connect to the robot and teleoperator
robot.connect()
teleop_device.connect()

# Init rerun viewer
init_rerun(session_name="phone_so100_teleop")

if not robot.is_connected or not teleop_device.is_connected:
    raise ValueError("Robot or teleop is not connected!")

print("Starting teleop loop. Move your phone to teleoperate the robot...")
while True:
    t0 = time.perf_counter()

    # Get robot observation
    robot_obs = robot.get_observation()

    # Get teleop action
    phone_obs = teleop_device.get_action()

    # Phone -> EE pose -> Joints transition
    joint_action = phone_to_robot_joints_processor((phone_obs, robot_obs))

    # Send action to robot
    _ = robot.send_action(joint_action)

    # 深拷贝，防止改到原始 phone_obs
    obs_scaled = copy.deepcopy(phone_obs)

    # 假设 phone_obs["phone"]["pos"] 是 numpy 数组或 list 放大100倍，方便在rerun上面观察
    obs_scaled["phone.pos"] = np.array(obs_scaled["phone.pos"]) * 100

    x, y, z = quaternion_to_euler(obs_scaled["phone.rot"])
    obs_scaled["phone.rot.x"] = x
    obs_scaled["phone.rot.y"] = y
    obs_scaled["phone.rot.z"] = z

    # Visualize
    log_rerun_data(observation=obs_scaled, action=joint_action)

    busy_wait(max(1.0 / FPS - (time.perf_counter() - t0), 0.0))
