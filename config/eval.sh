#!/bin/bash

#rm -rf /home/it/Desktop/lerobot/open_close1

#python lerobot/scripts/control_robot.py \
#  --control.single_task='关闭洗碗机的门' \
#  --robot.type=so100 \
#  --control.type=record \
#  --control.fps=30 \
#  --control.repo_id=lbg/eval_cleartab \
#  --control.tags='["tutorial"]' \
#  --control.warmup_time_s=5 \
#  --control.episode_time_s=500 \
#  --control.reset_time_s=10 \
#  --control.num_episodes=2 \
#  --control.push_to_hub=false \
#  --control.policy.path=outputs/train/2025-05-22-22-28/act_koch_test/checkpoints/last/pretrained_model \
#  --control.root=/home/it/Desktop/lerobot/open_close1 \
#  --control.display_data=false \
#  --control.policy.device='cuda'
#python lerobot/scripts/control_robot.py \
#  --control.single_task='打开洗碗机的门' \   #任务描述
#  --robot.type=so100 \    # 使用koch机器人
#  --control.type=record \  #录制
#  --control.fps=30 \    # 帧率，视频，电机等
#  --control.repo_id=lbg/cleartab \   # hub上面的id，也是任务的id
#  --control.tags='["tutorial"]' \  #如果上传的hub，使用tag的名称
#  --control.warmup_time_s=5 \    # 热机时间
#  --control.episode_time_s=100 \  # 录制时长
#  --control.reset_time_s=10 \    # 录制完成过后，恢复环境的时间，如：摆放碗盘
#  --control.num_episodes=2 \     # 录制次数
#  --control.push_to_hub=false \  # 是否推送的hub
#  --control.policy.path=outputs/train/2025-05-22-22-28/act_koch_test/checkpoints/last/pretrained_model \   # 模型路径
#  --control.root=/home/it/Desktop/lerobot/open_close1 \   #保存的文件路径
#  --control.display_cameras=false \  # 是否显示摄像头画面，打开报错
#  --control.device=cuda          # cpu推理
##  --control.policy.type=act \

source /home/it/anaconda3/etc/profile.d/conda.sh
conda activate lerobot

rm -rf /home/it/Desktop/lerobot/eval_test

#python -m lerobot.record --config_path=./config/so100/eval.yaml
echo "Python 路径: $(which python)"

if [ "$1" = "release" ]; then
  python -m lerobot.record --config_path=./config/lekiwi_car/eval.yaml \
    --policy.path=/backup/lerobots/lbg/lerobot/outputs/train/2025-09-23-18-38/act_koch_test1/checkpoints/010000/pretrained_model
else
  python -m lerobot.record --config_path=./config/lekiwi_car/eval.yaml \
    --policy.path=/backup/lerobots/lbg/lerobot/outputs/train/2025-09-29-19-45/act_koch_test1/checkpoints/040000/pretrained_model
fi
