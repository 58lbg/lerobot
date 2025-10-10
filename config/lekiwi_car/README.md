# 这个是给大象agv上面的lerobot机械臂使用的
# 遥控
先在树莓派上面运行：
```bash
ssh -Y er@10.253.58.135  #Elephant
cd Documents/lerobot
source ~/miniconda3/bin/activate
conda activate lerobot
python -m lerobot.common.robots.lekiwi_car.lekiwi_car_host
```
远程遥控: 在控制方上运行
```bash
python examples/lekiwi/teleoperate.py
```
# 数据录制
在树莓派上面运行：
```bash
ssh -Y er@10.253.58.135  #Elephant
cd Documents/lerobot
source ~/miniconda3/bin/activate
conda activate lerobot
python -m lerobot.common.robots.lekiwi_car.lekiwi_car_host
```
录制数据: 在控制方执行的命令
```bash
sh config/record.sh
```

# 训练
训练需要将采集数据拷贝到55，然后使用congfing/train.sh命令训练
拷贝命令, 将采集数据move_bowl，拷贝到55的Desktop/lerobot/下面，确保55里面没有move_bowl，有就删除，密码
lbg@5858
```bash
scp -r outputs/record/move_bowl/ it@10.253.104.55:/home/it/Desktop/lerobot/
```

修改config/train.sh中的：
```bash
#上传本地数据集到远程/
cp -r /home/it/Desktop/lerobot/lekiwi_move_boll/ /home/it/.cache/huggingface/lerobot/lbg/test/
```
/home/it/Desktop/lerobot/lekiwi_move_boll/目录改成对于拷贝的目录：
/home/it/Desktop/lerobot/move_bowl/

最后在项目根目录执行：
```bash
sh config/train.sh
```
注意：除了第一步的上传是在采集电脑执行外，其他都是在55上执行

# 可视化数据

```bash
python -m lerobot.scripts.visualize_dataset \
    --repo-id=lbg/cleartab \
    --episode-index=4 \
    --root=outputs/record/interaction
```

## 手柄控制

roslaunch myagv_navigation navigation_active.launch 
roslaunch myagv_ps2 myagv_ps2.launch