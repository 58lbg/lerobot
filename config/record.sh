#!/bin/bash

#python -m lerobot.record \
#    --robot.type=so100_follower \
#    --robot.port=/dev/ttyACM1 \
#    --robot.id=so100_right_follower \
#    --robot.cameras="{ front: {type: opencv, index_or_path: 0, width: 1920, height: 1080, fps: 30}}" \
#    --teleop.type=so100_leader \
#    --teleop.port=/dev/ttyACM0 \
#    --teleop.id=so100_right_leader \
#    --display_data=true \
#    --dataset.push_to_hub=false \
#    --dataset.episode_time_s=500 \
#    --dataset.reset_time_s=100 \
#    --dataset.repo_id="lbg/cleartab" \
#    --dataset.num_episodes=2 \
#    --dataset.single_task="lbgtask" \
#    --dataset.root="/home/it/Desktop/lerobot/test" \
#    --resume=false
if [ "$1" = "test" ]; then
  echo "测试录制"
  rm -rf ./outputs/record/test
  python -m lerobot.record --config_path=./config/lekiwi_car/record.yaml --resume=false --dataset.root=./outputs/record/test
  echo "clear test"
#  rm -rf ./outputs/record/test
else
  echo "正常录制"
  python -m lerobot.record --config_path=./config/lekiwi_car/record.yaml
fi