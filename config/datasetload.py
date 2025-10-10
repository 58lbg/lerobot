#!/usr/bin/env python

"""
LeRobot 数据集下载工具

这个工具用于从 Hugging Face 下载和加载 LeRobot 数据集。它提供了多种下载选项，
包括选择特定 episodes、是否下载视频文件、指定存储路径等。

使用方法：

1. 列出所有可用的数据集：
   python config/datasetload.py --list

2. 下载所有可用的数据集（后台运行）：
   python config/datasetload.py --download-all --background
   python config/datasetload.py --download-all --root /path/to/store --background
   python config/datasetload.py --download-all --no-videos --background

3. 下载完整数据集：
   python config/datasetload.py --repo-id lerobot/aloha_mobile_cabinet

4. 下载特定 episodes：
   python config/datasetload.py --repo-id lerobot/aloha_mobile_cabinet --episodes 0,1,2

5. 指定本地存储路径：
   python config/datasetload.py --repo-id lerobot/aloha_mobile_cabinet --root /path/to/store

6. 不下载视频文件：
   python config/datasetload.py --repo-id lerobot/aloha_mobile_cabinet --no-videos

7. 指定数据集版本：
   python config/datasetload.py --repo-id lerobot/aloha_mobile_cabinet --revision v1.0

参数说明：
--list: 列出所有可用的数据集
--download-all: 下载所有可用的数据集
--background: 在后台运行下载任务
--repo-id: 要下载的数据集仓库 ID（单个数据集下载时必需）
--root: 本地存储路径，默认为 HF_LEROBOT_HOME/repo_id
--episodes: 要下载的特定 episodes，用逗号分隔的数字列表
--no-videos: 不下载视频文件
--revision: 数据集版本（分支、标签或提交哈希）

下载完成后会显示数据集的基本信息：
- 数据集 ID
- 本地存储路径
- episodes 数量
- 帧数
- FPS
- 可用的特征列表

注意：
1. 首次下载数据集时可能需要一些时间，特别是当数据集包含视频文件时
2. 确保有足够的磁盘空间来存储数据集
3. 需要稳定的网络连接来下载数据集
4. 下载所有数据集时，如果某个数据集下载失败，会继续下载其他数据集
5. 如果下载过程中断，可以重新运行命令，它会继续下载未完成的数据集
6. 后台下载的日志会保存在 outputs/download.log 文件中
"""

import argparse
import logging
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Optional

from huggingface_hub import HfApi, snapshot_download
from lerobot.common.datasets.lerobot_dataset import LeRobotDataset, LeRobotDatasetMetadata
from lerobot.common.constants import HF_LEROBOT_HOME

# 设置日志
def setup_logging():
    """设置日志记录"""
    log_dir = Path("outputs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "download.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

def download_dataset(
    repo_id: str,
    root: Optional[str] = None,
    episodes: Optional[List[int]] = None,
    download_videos: bool = True,
    revision: Optional[str] = None,
) -> LeRobotDataset:
    """
    下载并加载 LeRobot 数据集
    
    Args:
        repo_id (str): Hugging Face 数据集仓库 ID
        root (Optional[str]): 本地存储路径，默认为 HF_LEROBOT_HOME/repo_id
        episodes (Optional[List[int]]): 要下载的特定 episodes，默认为全部下载
        download_videos (bool): 是否下载视频文件，默认为 True
        revision (Optional[str]): 数据集版本，默认为最新版本
        
    Returns:
        LeRobotDataset: 加载好的数据集对象
    """
    # 设置本地存储路径
    if root is None:
        root = str(HF_LEROBOT_HOME / repo_id)
    else:
        root = root + "/" + repo_id
    # 创建数据集对象
    dataset = LeRobotDataset(
        repo_id=repo_id,
        root=root,
        episodes=episodes,
        download_videos=download_videos,
        revision=revision
    )
    
    return dataset


def list_available_datasets() -> None:
    """列出所有可用的 LeRobot 数据集"""
    hub_api = HfApi()
    repo_ids = [info.id for info in hub_api.list_datasets(task_categories="robotics", tags=["LeRobot",'so100'])]
    print("Available LeRobot datasets:")
    for repo_id in repo_ids:
        print(f"- {repo_id}")


def download_all_datasets(root: Optional[str] = None, download_videos: bool = True) -> None:
    """
    下载所有可用的 LeRobot 数据集
    
    Args:
        root (Optional[str]): 本地存储路径，默认为 HF_LEROBOT_HOME
        download_videos (bool): 是否下载视频文件，默认为 True
    """
    hub_api = HfApi()
    repo_ids = [info.id for info in hub_api.list_datasets(task_categories="robotics", tags=["LeRobot",'so100'])]
    
    logger.info(f"Found {len(repo_ids)} datasets to download")
    
    success_count = 0
    error_count = 0
    error_datasets = []
    
    for i, repo_id in enumerate(repo_ids, 1):
        time.sleep(1)
        logger.info(f"\nDownloading dataset {i}/{len(repo_ids)}: {repo_id}")
        try:
            # 推测数据集下载后保存目录为 root/repo_id
            local_path = Path(root or HF_LEROBOT_HOME) / repo_id
            # 如果目录已存在，跳过
            if local_path.exists():
                logger.info(f"Skipping {repo_id} (already exists at {local_path})")
                success_count += 1
                continue

            dataset = download_dataset(
                repo_id=repo_id,
                root=root,
                download_videos=download_videos
            )
            success_count += 1
            logger.info(f"Successfully downloaded {repo_id}")
            logger.info(f"Local path: {dataset.root}")
            logger.info(f"Number of episodes: {dataset.num_episodes}")
            logger.info(f"Number of frames: {dataset.num_frames}")
        except Exception as e:
            time.sleep(1)
            error_count += 1
            error_datasets.append(repo_id)
            logger.error(f"Error downloading {repo_id}: {str(e)}")
            # 推测数据集下载后保存目录为 root/repo_id
            local_path = Path(root or HF_LEROBOT_HOME) / repo_id
            # 删除可能已创建的本地文件夹
            if local_path.exists():
                try:
                    shutil.rmtree(local_path)
                    logger.info(f"Deleted partial download at {local_path}")
                    if local_path.parent.exists() and not any(local_path.parent.iterdir()):
                        shutil.rmtree(local_path.parent)
                except Exception as del_err:
                    logger.warning(f"Failed to delete {local_path}: {str(del_err)}")
            # if error_count > 20:
            #     break
            logger.info("Continuing with next dataset...")
            continue

    # 打印下载总结
    logger.info("\nDownload Summary:")
    logger.info(f"Total datasets: {len(repo_ids)}")
    logger.info(f"Successfully downloaded: {success_count}")
    logger.info(f"Failed to download: {error_count}")
    if error_count > 0:
        logger.info("\nFailed datasets:")
        for repo_id in error_datasets:
            logger.info(f"- {repo_id}")
        logger.info("\nYou can retry downloading failed datasets later.")


def run_in_background():
    """在后台运行下载任务"""
    # 获取当前脚本的路径
    script_path = os.path.abspath(__file__)
    
    # 构建命令
    cmd = [
        sys.executable,  # 使用当前 Python 解释器
        script_path,
        "--download-all"
    ]
    
    # 添加其他参数
    if args.root:
        cmd.extend(["--root", args.root])
    if args.no_videos:
        cmd.append("--no-videos")
    
    # 在后台运行命令
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True
    )
    
    logger.info(f"Started background download process with PID: {process.pid}")
    logger.info("You can check the progress in outputs/download.log")
    logger.info("Use 'cat outputs/download.log' to view the progress")


def main():
    parser = argparse.ArgumentParser(description="LeRobot Dataset Download Tool")
    parser.add_argument("--list", action="store_true", help="List all available datasets")
    parser.add_argument("--download-all", default=True,  action="store_true", help="Download all available datasets")
    parser.add_argument("--background", default=False, action="store_true", help="Run download in background")
    parser.add_argument("--repo-id", type=str, help="Dataset repository ID to download")
    parser.add_argument("--root", default="/media/it/Elements/so100-dataset/", type=str, help="Local directory to store the dataset")
    parser.add_argument("--episodes", type=str, help="Comma-separated list of episode indices to download")
    parser.add_argument("--no-videos", action="store_true", help="Do not download video files")
    parser.add_argument("--revision", type=str, help="Dataset revision (branch, tag or commit hash)")
    
    global args
    args = parser.parse_args()
    
    if args.list:
        list_available_datasets()
        return
    
    if args.download_all:
        if args.background:
            run_in_background()
        else:
            download_all_datasets(root=args.root, download_videos=not args.no_videos)
        return
    
    if not args.repo_id:
        print("Error: --repo-id is required")
        return
    
    # 解析 episodes
    episodes = None
    if args.episodes:
        episodes = [int(ep) for ep in args.episodes.split(",")]
    
    # 下载数据集
    dataset = download_dataset(
        repo_id=args.repo_id,
        root=args.root,
        episodes=episodes,
        download_videos=not args.no_videos,
        revision=args.revision
    )
    
    # 打印数据集信息
    logger.info(f"\nDataset loaded successfully:")
    logger.info(f"Repository ID: {dataset.repo_id}")
    logger.info(f"Local path: {dataset.root}")
    logger.info(f"Number of episodes: {dataset.num_episodes}")
    logger.info(f"Number of frames: {dataset.num_frames}")
    logger.info(f"FPS: {dataset.fps}")
    logger.info(f"Features: {list(dataset.features.keys())}")


if __name__ == "__main__":
    main()
