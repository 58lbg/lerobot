#!/bin/bash

#设备定义，可以指定设备名称， 在根目录执行：
# sh config/record.sh koch
# sh config/record.sh sm100
# 如果不传参数，则使用默认值

KOCH="koch"
SO100="so100"

ROBOT_TYPE=$SO100

#echo "constants: $1"

if [ "$1" = "$KOCH" ]; then
    ROBOT_TYPE=$KOCH
elif [ "$1" = "$SO100" ]; then
    ROBOT_TYPE=$SO100
fi
