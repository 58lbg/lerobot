#!/bin/bash

source /home/it/anaconda3/etc/profile.d/conda.sh
source /home/it/.bashrc


cd /backup/lerobots/lbg/lerobot-dataset-test/lerobot
conda activate lerobot310
git pull

python config/datasetload.py