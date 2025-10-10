#!/bin/bash

which python

remove() {
    double=$1
    for ((i=357; i>=0; i--)); do
        if [ "$double" = true ]; then
            # 输出偶数
            if (( i % 2 == 0 )); then
              python3 -m config.utils.dataset_tool_cli  delete \
                --dataset_dir  /home/it/Desktop/lerobot/lekiwi_car_release\
                --episode_id "$i"
            fi
        else
            # 输出奇数
            if (( i % 2 == 1 )); then
              python3 -m config.utils.dataset_tool_cli  delete \
                --dataset_dir  /home/it/Desktop/lerobot/lekiwi_car_grap\
                --episode_id "$i"
            fi
        fi
    done
}

# 调用：传入 true 输出偶数，false 输出奇数
remove false