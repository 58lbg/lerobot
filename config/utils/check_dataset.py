import os
import cv2
import pyarrow.parquet as pq

def check_lerobot_dataset(root, camera="observation.images.laptop"):
    data_root = os.path.join(root, "data")
    video_root = os.path.join(root, "videos")

    total, ok, err = 0, 0, 0

    for chunk in sorted(os.listdir(data_root)):
        chunk_path = os.path.join(data_root, chunk)
        if not os.path.isdir(chunk_path):
            continue

        video_chunk_path = os.path.join(video_root, chunk, camera)
        if not os.path.exists(video_chunk_path):
            print(f"[WARN] {chunk} 缺少相机目录 {camera}")
            continue

        for fname in sorted(os.listdir(chunk_path)):
            if not fname.endswith(".parquet"):
                continue

            ep_name = fname.replace(".parquet", "")
            parquet_file = os.path.join(chunk_path, fname)
            video_file = os.path.join(video_chunk_path, f"{ep_name}.mp4")

            if not os.path.exists(video_file):
                print(f"[WARN] {ep_name} 缺少视频文件 {video_file}")
                continue

            # --- 1. 读取 episode 长度 ---
            table = pq.read_table(parquet_file)
            step_len = table.num_rows

            # --- 2. 读取 mp4 帧数 ---
            cap = cv2.VideoCapture(video_file)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            cap.release()

            # --- 3. 对比 ---
            total += 1
            if step_len == frame_count:
                print(f"[OK] {ep_name}: step={step_len}, frame={frame_count}")
                ok += 1
            else:
                print(f"[ERROR] {ep_name}: step={step_len}, frame={frame_count}")
                err += 1

    print("\n=== 统计结果 ===")
    print(f"总集数: {total}, 一致: {ok}, 不一致: {err}")

# 用法
if __name__ == "__main__":
    check_lerobot_dataset("/home/it/Desktop/lerobot/lekiwi_car_grap_release/", camera="observation.images.top")