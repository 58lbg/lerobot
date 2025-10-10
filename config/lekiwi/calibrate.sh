#folower
python -m lerobot.calibrate \
    --robot.type=lekiwi \
    --robot.id=lbg_kiwi \
    --robot.calibration_dir=.cache/calibration/lekiwi

#leader
#python -m lerobot.calibrate \
#    --teleop.type=so100_leader \
#    --teleop.port=/dev/ttyACM0 \
#    --teleop.calibration_dir=.cache/calibration/lekiwi \
#    --teleop.id=so100_right_leader