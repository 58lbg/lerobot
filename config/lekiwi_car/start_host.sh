#!/bin/bash
cd ~/Documents/lerobot
source ~/miniconda3/bin/activate
conda activate lerobot
echo "Python 路径: $(which python)"
python -m lerobot.common.robots.lekiwi_car.lekiwi_car_host

exit_code=$?
echo "$exit_code"
exit $exit_code