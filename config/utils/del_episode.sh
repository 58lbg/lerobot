#!/bin/bash



# 使用序列表达式 {1..5}
for i in {60..0}
do
  python3 -m config.utils.dataset_tool_cli  delete \
      --verbose \
      --dataset_dir  /home/it/Desktop/lerobot/move_bowl_camera_key/ \
      --episode_id $i \
      --verbose
done

