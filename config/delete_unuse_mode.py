import os
import re
import shutil
import sys


def delete_old_checkpoints(root_dir):
    # 定义一个正则表达式来匹配文件夹名，如 020000, 040000 等
    folder_pattern = re.compile(r'^\d{6}$')

    # 遍历给定文件夹的所有目录
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 检查当前路径是否包含 'checkpoints' 目录
        if 'checkpoints' in dirnames:
            checkpoints_dir = os.path.join(dirpath, 'checkpoints')
            # 获取所有子文件夹
            subfolders = [f for f in os.listdir(checkpoints_dir) if os.path.isdir(os.path.join(checkpoints_dir, f))]
            # 只选择符合模式的文件夹（020000, 040000 等）
            valid_folders = [f for f in subfolders if folder_pattern.match(f)]

            # 如果valid_folders不为空，则处理它们
            if valid_folders:
                # 将valid_folders按数字顺序排序
                valid_folders.sort(key=lambda x: int(x))

                # 删除序号较小的文件夹
                for folder in valid_folders[:-1]:  # 保留最后一个文件夹
                    folder_path = os.path.join(checkpoints_dir, folder)
                    print(f"Deleting folder: {folder_path}")
                    shutil.rmtree(folder_path)

                # 保留最大的文件夹和 'last' 文件夹
                last_folder = 'last'
                last_folder_path = os.path.join(checkpoints_dir, last_folder)
                if os.path.isdir(last_folder_path):
                    print(f"Keeping 'last' folder: {last_folder_path}")
                else:
                    print(f"'last' folder does not exist, nothing to keep.")

                max_folder = valid_folders[-1]
                max_folder_path = os.path.join(checkpoints_dir, max_folder)
                print(f"Keeping folder: {max_folder_path}")

    print("Finished processing the directories.")

if __name__ == "__main__":
    # 检查是否传入了路径参数
    if len(sys.argv) < 2:
        print("Usage: python script.py <folder_path>")
        sys.exit(1)

    # 获取命令行输入的路径
    root_dir = sys.argv[1]

    # 检查路径是否存在
    if not os.path.exists(root_dir):
        print(f"Error: The path '{root_dir}' does not exist.")
        sys.exit(1)
    # 继续执行你的逻辑
    print(f"Processing folder: {root_dir}")

    delete_old_checkpoints(root_dir)