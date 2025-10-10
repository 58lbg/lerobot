from config.constants import KOCH, SO100, ROBOT_TYPE
from lerobot.common.policies.act.modeling_act import ACTPolicy
from lerobot.common.policies.diffusion.modeling_diffusion import DiffusionPolicy
from lerobot.common.policies.smolvla.modeling_smolvla import SmolVLAPolicy
from lerobot.common.policies.vqbet.modeling_vqbet import VQBeTPolicy
from lerobot.common.robot_devices.robots.configs import KochRobotConfig, So100RobotConfig, ManipulatorRobotConfig
from lerobot.common.robot_devices.robots.manipulator import ManipulatorRobot
from lerobot.scripts.control_robot import busy_wait
import time
import torch

#可以指定设备名称， 在根目录制作：
# python3 -m config.eval koch
# python3 -m config.eval sm100

inference_time_s = 160
fps = 30
device = "cuda"  # TODO: On Mac, use "mps" or "cpu" “cuda”
# ckpt_path = "outputs/train/2025-06-06-16-45/act_koch_test/checkpoints/040000/pretrained_model"
ckpt_path = "outputs/train/2025-06-11-22-36/act_koch_test/checkpoints/005000/pretrained_model"
#ckpt_path = "outputs/train/2025-05-26-20-44/diffusion_koch_test/checkpoints/100000/pretrained_model"
#policy = DiffusionPolicy.from_pretrained(ckpt_path)
# 从路径加载模型和配置
# policy = ACTPolicy.from_pretrained(ckpt_path)
policy = SmolVLAPolicy.from_pretrained(ckpt_path)
#policy = VQBeTPolicy.from_pretrained(ckpt_path)
policy.to(device)

# 机器配置、电机、摄像头等
#koch
if ROBOT_TYPE == KOCH:
    robot_config = KochRobotConfig()
    robot = ManipulatorRobot(robot_config)
#sm-l00
else:
    robot_config = So100RobotConfig()
    robot = ManipulatorRobot(robot_config)
# 电机的对象为DynamixelMotorsBus，连接过后会锁定从动臂；（锁力矩、主动臂配置回弹）
robot.connect()

for _ in range(inference_time_s * fps):
    start_time = time.perf_counter()

    # Read the follower state and access the frames from the cameras
    observation = robot.capture_observation()

    with (
        torch.inference_mode(),
        torch.autocast(device_type=device)
    ):

        # Convert to pytorch format: channel first and float32 in [0,1]
        # with batch dimension
        for name in observation:
            if "image" in name:
                # 归一化
                observation[name] = observation[name].type(torch.float32) / 255
                # 维度转换：HWC → CHW ，contiguous内存布局连续
                observation[name] = observation[name].permute(2, 0, 1).contiguous()
            # 添加 Batch 维度
            observation[name] = observation[name].unsqueeze(0)
            # 移动到 GPU 或 CPU
            observation[name] = observation[name].to(device)

        # Compute the next action with the policy
        # based on the current observation
        action = policy.select_action(observation)
        print(f"======================={time.perf_counter() - start_time}")
        # Remove batch dimension
        action = action.squeeze(0)
        # Move to cpu, if not already the case
        action = action.to("cpu")
        # Order the robot to move
        robot.send_action(action)

        dt_s = time.perf_counter() - start_time
        print("-------------------------")
        dely = 1 / fps - dt_s
        busy_wait(dely)
        print(f"=======================")
