# 命令

```bash
ssh -Y er@10.253.58.135  #Elephant
cd Documents/lerobot
source ~/miniconda3/bin/activate
conda activate lerobot
python -m config.lekiwi_car.task_demo.move_task
python -m roslaunch myagv_navigation navigation_active.launch
python -m config.lekiwi_car.task_demo.wss_client_55
```