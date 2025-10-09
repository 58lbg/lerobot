# 该目录是执行数据采集、推理、执行、数据可视化相关操作的脚本目。

## shell脚本 传入设备名称
设备定义，可以指定设备名称，在根目录执行：
```bash
 sh config/record.sh koch
 sh config/record.sh sm100
# 或者修改默认值
```

## python执行方式  传入设备名称
设备定义，如执行评估的python文件，可以指定设备名称， 在根目录执行：
```bash
python3 -m config.eval koch
python3 -m config.eval sm100
# 如果不加参数则使用默认值
```

## 重启过去摄像头和电机的位置端口号不对，需要重新配置
```bash
#查看所有的设备，然后拔一个，执行一下，就知道对应的设备了
ll /dev/ttyACM*  
#摄像头使用下面命令，然后去目录看摄像头编号，然后配置对应的编号
python -m lerobot.find_cameras opencv
# 如果不加参数则使用默认值
# 查看摄像头分辨率/ fps等
v4l2-ctl -d /dev/video0 --list-formats-ext
```


## 校准
跟随臂
```bash
python -m lerobot.calibrate \
    --robot.type=so100_follower \
    --robot.port=/dev/ttyACM1 \
    --robot.calibration_dir=/backup/lerobots/lbg/lerobot/.cache/calibration/so100 \
    --robot.id=so100_right_follower
```
领导臂
```bash
python -m lerobot.calibrate \
    --teleop.type=so100_leader \
    --teleop.port=/dev/ttyACM0 \
    --teleop.calibration_dir=/backup/lerobots/lbg/lerobot/.cache/calibration/so100 \
    --teleop.id=so100_right_leader
```

## 归0,并设置编号
```bash
python -m lerobot.setup_motors \
    --robot.type=so100_follower \
    --robot.port=/dev/ttyACM0  # <- paste here the port found at previous step
```

## Merge multiple sessions

If you record data over several sessions (different days, tasks, or robots) you may want to combine them into a single dataset directory so that training and evaluation scripts.

```bash
python3 -m config.utils.dataset_tool_cli merge  \
      --verbose \
      --datasets "/home/it/Desktop/lerobot/diff-desk-white/ /home/it/Desktop/lerobot/diff-desk/" \
      --output_dir /home/it/Desktop/lerobot/diff-desk-all
```

## Delete a specific episode

You can also delete a specific episode from a dataset, for example to remove faulty or irrelevant data:

```bash
python3 -m config.utils.dataset_tool_cli  delete \
      --verbose \
      --dataset_dir  /home/it/Desktop/lerobot/lekiwi_car_grap\
      --episode_id 40 \
      --verbose
```

## 电脑之间传数据:
```bash
scp -r outputs/record/move_bowl_*/  it@10.253.104.55:/home/it/Desktop/lerobot/
scp -r it@10.253.104.55:/home/it/Desktop/lerobot/move_bowl_key outputs/record
```

## 查看摄像头支持的分辨率
```bash
v4l2-ctl --list-formats-ext -d /dev/video0
```

## 其它
参考网站：
https://huggingface.co/docs/lerobot/en/so101
wget https://diffusion-policy.cs.columbia.edu/data/training/robomimic_image.zip
python3 -m config.utils.dataset_tool_cli merge --datasets "/home/it/Desktop/lerobot/xi_wan_ji_ci_wan /home/it/Desktop/lerobot/task_yan_zheng_wei_quan_bu_yi_yang" --output_dir /home/it/Desktop/lerobot/xi_wan_ji_all

当前项目编译使用如下命令：
pip install -e ".[feetech, pusht]"
其中feetech为使用电机型号

## 应用校准文件, 需要先修改里面的配置
python -m config.utils.reset_motor apply

## 恢复电机的offset=0， max angele=4095 mix angle=0
python -m config.utils.reset_motor reset