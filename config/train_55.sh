#!/bin/bash

source /home/it/anaconda3/etc/profile.d/conda.sh
source /home/it/.bashrc

#这个是55执行训练的脚本
#这个需要在10.253.104.55机器上运行，远程登录过后这样执行
#没有日志
#nohup bash config/train_55.sh so100 > /dev/null 2>&1 &
#日志
#nohup bash config/train_55.sh so100 > outputs/log-all.txt 2>&1 &
#延时7小时执行
#echo "nohup bash config/train_55.sh > outputs/log-all.txt 2>&1 &" | at now + 7 hours
cd /backup/lerobots/lbg/lerobot
conda activate lerobot
git pull
mkdir -p outputs

. ./config/constants.sh "$1"

current_time=$(date +"%Y-%m-%d-%H-%M")
path=outputs/train/$current_time

mkdir -p "$path"

resume=false
if [ "$resume" = "true" ]; then
  #恢复训练并设置步数,需要知道模型的位置
  python lerobot/scripts/train.py \
      --config_path=outputs/train/2025-06-09-19-10/act_koch_test/checkpoints/200000/pretrained_model \
      --resume=true \
      --steps=60000 >> "$path/log_act_policy.txt" 2>&1

else
  #act
#  python lerobot/scripts/train.py \
#    --steps=20000 \
#    --save_freq=1000 \
#    --batch_size=32 \
#    --dataset.repo_id=lbg/test \
#    --policy.type=act \
#    --output_dir="$path/act_koch_test1" \
#    --seed=1000 \
#    --job_name=act_koch_test \
#    --policy.n_action_steps=100 \
#    --wandb.enable=false > "$path/log_act1.txt" 2>&1

#  python lerobot/scripts/train.py \
#    --steps=20000 \
#    --save_freq=1000 \
#    --batch_size=32 \
#    --dataset.repo_id=lbg/test \
#    --policy.type=act \
#    --output_dir="$path/act_koch_test2" \
#    --seed=1100 \
#    --job_name=act_koch_test \
#    --policy.n_action_steps=100 \
#    --wandb.enable=false > "$path/log_act2.txt" 2>&1

  python lerobot/scripts/train.py \
    --steps=100000 \
    --save_freq=10000 \
    --batch_size=16 \
    --dataset.repo_id=lbg/test \
    --policy.type=act \
    --output_dir="$path/act_koch_test1" \
    --seed=1200 \
    --job_name=act_koch_test \
    --policy.n_action_steps=100 \
    --wandb.enable=false > "$path/log_act1.txt" 2>&1

  #先删除远程的文件 ~/.cache/huggingface/lerobot/lbg/test/s
  rm -rf /home/it/.cache/huggingface/lerobot/lbg/test/

  #上传本地数据集到远程/
  cp -r /home/it/Desktop/lerobot/lekiwi_car_release/ /home/it/.cache/huggingface/lerobot/lbg/test/

  python lerobot/scripts/train.py \
    --steps=100000 \
    --save_freq=10000 \
    --batch_size=16 \
    --dataset.repo_id=lbg/test \
    --policy.type=act \
    --output_dir="$path/act_koch_test2" \
    --seed=1200 \
    --job_name=act_koch_test \
    --policy.n_action_steps=100 \
    --wandb.enable=false > "$path/log_act2.txt" 2>&1


#  python lerobot/scripts/train.py \
#    --steps=70000 \
#    --save_freq=10000 \
#    --batch_size=16 \
#    --dataset.repo_id=lbg/test \
#    --policy.type=act \
#    --policy.vision_backbone='resnet50' \
#    --policy.pretrained_backbone_weights='ResNet50_Weights.IMAGENET1K_V1' \
#    --policy.replace_final_stride_with_dilation=false \
#    --policy.replace_final_stride_with_dilation_second=false \
#    --output_dir="$path/act_koch_test3" \
#    --seed=1100 \
#    --job_name=act_koch_test \
#    --policy.n_action_steps=100 \
#    --wandb.enable=false > "$path/log_act3.txt" 2>&1
#  python lerobot/scripts/train.py \
#    --steps=30000 \
#    --save_freq=5000 \
#    --batch_size=16 \
#    --dataset.repo_id=lbg/test \
#    --policy.type=act \
#    --policy.vision_backbone='resnet34' \
#    --policy.pretrained_backbone_weights='ResNet34_Weights.IMAGENET1K_V1' \
#    --output_dir="$path/act_koch_test4" \
#    --seed=1000 \
#    --job_name=act_koch_test \
#    --policy.n_action_steps=100 \
#    --wandb.enable=false > "$path/log_act4.txt" 2>&1

  #act 微调
#  python lerobot/scripts/train.py \
#    --steps=100000 \
#    --save_freq=20000 \
#    --batch_size=16 \
#    --dataset.repo_id=lbg/test \
#    --policy.path=outputs/train/2025-06-10-17-00/act_koch_test/checkpoints/150000/pretrained_model \
#    --output_dir="$path/act_koch_test" \
#    --job_name=act_koch_test \
#    --wandb.enable=false > "$path/log_act_policy.txt" 2>&1

    #steps 训练步数
    #dataset.repo_id 在~/.cache/huggingface/lerobot/ 目录下的id，如果配置了huggingface的账号，会上传
    #policy.path 微调模型的路径
    #output_dir 输入模型路径
    #save_freq 没多少步输出一下模型

  #smolvla
#  python lerobot/scripts/train.py \
#    --policy.path=lerobot/smolvla_base \
#    --steps=50000 \
#    --save_freq=5000 \
#    --batch_size=32 \
#    --dataset.repo_id=lbg/test \
#    --output_dir="$path/act_koch_test" \
#    --job_name=act_koch_test \
#    --wandb.enable=false > "$path/log_act_policy.txt" 2>&1

#  python lerobot/scripts/train.py \
#    --policy.type=smolvla \
#    --steps=50000 \
#    --save_freq=5000 \
#    --batch_size=32 \
#    --dataset.repo_id=lbg/test \
#    --output_dir="$path/act_koch_test" \
#    --job_name=act_koch_test \
#    --wandb.enable=false > "$path/log_act_policy.txt" 2>&1

  #diffusion
  #python lerobot/scripts/train.py \
  #  --steps=600000 \
  #  --batch_size=24 \
  #  --save_freq=50000 \
  #  --dataset.repo_id=lbg/xi_wan_ji_ci_wan \
  #  --n_action_steps=100 \
  #  --policy.type=diffusion \
  #  --output_dir="$path/diffusion_koch_test" \
  #  --job_name=diffusion_koch_test \
  #  --wandb.enable=false > "$path/log_diffusion.txt" 2>&1

  #vqbet
  #python lerobot/scripts/train.py \
  #  --dataset.repo_id=lbg/test \
  #  --policy.type=vqbet \
  #  --output_dir="$path/vqbet_koch_test" \
  #  --job_name=vqbet_koch_test \
  #  --device=cuda \
  #  --wandb.enable=false \
  #  --dataset.local_files_only=true > "$path/log.txt" 2>&1
fi

#训练完了过后，传到177
if [ "$KOCH" = "$ROBOT_TYPE" ]; then
    sshpass -p 55558888 scp -r "$path"  oem-2@10.253.66.177:/home/oem-2/文档/lerobot/outputs/train/$current_time/
#else
#    sshpass -p asdf scp -r outputs/train/$current_time/  luxing@10.253.82.80:/home/luxing/lerobot/outputs/train/$current_time/
fi
