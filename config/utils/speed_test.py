from pathlib import Path

from lerobot.common.robots.lekiwi import LeKiwiConfig, lekiwi, LeKiwi

robot_config = LeKiwiConfig()
robot_config.calibration_dir = Path("/backup/lerobots/lbg/lerobot-lekiwi/.cache/calibration/lekiwi")
robot_config.id = "lbg_kiwi"
robot = LeKiwi(robot_config)

print(robot._body_to_wheel_raw(0.1, 0, 0))
print(robot._wheel_raw_to_body(-1129, 0, 1129))