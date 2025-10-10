# 杀死占用 /dev/ttyACM0 的进程
sudo fuser -k /dev/ttyACM0 2>/dev/null

# 重置串口（部分设备需要）
sudo stty -F /dev/ttyACM0 sane

# 启动程序
python -m lerobot.common.robots.lekiwi.lekiwi_host