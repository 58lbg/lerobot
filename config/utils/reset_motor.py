import sys
from pathlib import Path

from lerobot.common.robots.so100_follower import SO100Follower, SO100FollowerConfig
from lerobot.common.teleoperators.so100_leader import SO100Leader, SO100LeaderConfig
from lerobot.common.robots.lekiwi import LeKiwiConfig, LeKiwi
from lerobot.common.motors.feetech import (
    FeetechMotorsBus,
)


so100_follower: SO100Follower | None = None
so100_leader: SO100Leader | None = None
leKiwi: LeKiwi | None = None
def init_robot():

    global so100_follower, so100_leader
    global leKiwi

    config = SO100FollowerConfig(
        port="/dev/ttyACM1",
        id="so100_right_follower",
        calibration_dir=Path(".cache/calibration/so100")
    )
    follower_100 = SO100Follower(config)


    # config = SO100LeaderConfig(
    #     port="/dev/ttyACM0",
    #     id="so100_right_leader",
    #     calibration_dir = Path(".cache/calibration/lekiwi")
    # )

    config = SO100LeaderConfig(
        port="/dev/ttyACM0",
        id="so100_lekiwi_car_leader",
        calibration_dir=Path(".cache/calibration/lekiwi_car")
    )
    leader_100 = SO100Leader(config)


    config = LeKiwiConfig(
        port="/dev/ttyACM0",
        id="lbg_kiwi",
        calibration_dir = Path(".cache/calibration/lekiwi")
    )
    leKiwi_temp = LeKiwi(config)

    # so100_follower = follower_100
    so100_leader = leader_100
    # leKiwi = leKiwi_temp

    if so100_follower is not None:
        so100_follower.connect(False)
    if so100_leader is not None:
        so100_leader.connect(False)
    if leKiwi is not None:
        leKiwi.connect(False)

def apply_all():
    if so100_follower is not None:
        so100_follower.rewrite_calibration()
    if so100_leader is not None:
        so100_leader.rewrite_calibration()
    if leKiwi is not None:
        leKiwi.rewrite_calibration()

def print_error_status():
    if so100_follower is not None:
        so100_follower.bus.print_error_status()
        print_motor_offset(so100_follower.bus)
    if so100_leader is not None:
        so100_leader.bus.print_error_status()
        print_motor_offset(so100_leader.bus)
    if leKiwi is not None:
        leKiwi.bus.print_error_status()
        print_motor_offset(leKiwi.bus)

def reset_all() :
    if so100_follower is not None:
        reset(so100_follower.bus)
    if so100_leader is not None:
        reset(so100_leader.bus)
    if leKiwi is not None:
        reset(leKiwi.bus)

def reset(bus : FeetechMotorsBus):
    for motor in bus.motors:
        bus.write("Homing_Offset", motor, 0)
        bus.write("Min_Position_Limit", motor, 0)
        bus.write("Max_Position_Limit", motor, 4095)
def print_motor_offset(bus : FeetechMotorsBus):
    for motor in bus.motors:
        offset_value = bus.read("Homing_Offset", motor)
        min = bus.read("Min_Position_Limit", motor)
        max = bus.read("Max_Position_Limit", motor)
        print(f"{motor} : offset {offset_value}; Min {min}; Max {max}")

if __name__ == "__main__":
    init_robot()
    if len(sys.argv) > 1:
        if sys.argv[1] == "apply":
            apply_all()
        if sys.argv[1] == "reset":
            reset_all()
    print_error_status()



