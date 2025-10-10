from lerobot.common.robots.so101_follower import SO101Follower, SO101FollowerConfig
from lerobot.common.robots.lekiwi import LeKiwiConfig, LeKiwi
from lerobot.common.teleoperators.so101_leader import SO101LeaderConfig, SO101Leader

config = SO101LeaderConfig(
    port="/dev/ttyACM1",
    id="right_leader_arm",
)
follower = SO101Leader(config)
follower.setup_motors()