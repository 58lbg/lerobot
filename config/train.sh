#!/bin/bash


#延时7小时执行
#echo "bash config/train.sh" | at now + 2 hours

#这个是本地调用远程执行训练的脚本

# 获取第一个命令行参数
password=$1

. ./config/constants.sh "$2"

echo "当前环境$ROBOT_TYPE"
echo "上传本地数据集..."
if [ "$KOCH" = "$ROBOT_TYPE" ]; then
    echo "1 正在删除远程缓存文件..."
    #先删除远程的文件 ~/.cache/huggingface/lerobot/lbg/test/
    sshpass -p "$password" ssh it@10.253.104.55 rm -rf /home/it/.cache/huggingface/lerobot/lbg/xi_wan_ji_ci_wan/
    #上传本地数据集到远程
    sshpass -p "$password" scp -r outputs/test it@10.253.104.55:/home/it/.cache/huggingface/lerobot/lbg/xi_wan_ji_ci_wan/

    echo "数据集上传完成..."

    echo "开始远程训练..."
    #执行远程的训练命令
    sshpass -p "$password" ssh it@10.253.104.55 nohup bash /backup/lerobots/lbg/lerobot/config/train_55.sh "$ROBOT_TYPE" > outputs/log-all.txt 2>&1 &
    echo "训练任务已启动，日志输出到 outputs/log-all.txt"

else
    echo "2 正在删除远程缓存文件..."
    #先删除远程的文件 ~/.cache/huggingface/lerobot/lbg/test/s
    rm -rf /home/it/.cache/huggingface/lerobot/lbg/test/

    #上传本地数据集到远程/
    cp -r /home/it/Desktop/lerobot/lekiwi_car_grap/ /home/it/.cache/huggingface/lerobot/lbg/test/

    echo "数据集上传完成..."

    echo "开始远程训练..."
    #执行远程的训练命令
    nohup bash ./config/train_55.sh "$ROBOT_TYPE" > outputs/log-all.txt 2>&1 &
    echo "训练任务已启动，日志输出到 outputs/log-all.txt"
fi


