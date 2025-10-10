#!/usr/bin/env python
import sys

#设备定义，如执行评估的python文件，可以指定设备名称， 在根目录执行：
# python3 -m config.eval koch
# python3 -m config.eval sm100
# 如果不加参数则使用默认值

KOCH = "koch"
SO100 = "so100"

ROBOT_TYPE = SO100

if len(sys.argv) > 1:
    first_input = sys.argv[1]  # 获取第一个参数
    if first_input == KOCH:
        ROBOT_TYPE = KOCH
    elif first_input == SO100:
        ROBOT_TYPE = SO100

