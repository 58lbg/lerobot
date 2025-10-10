import pandas as pd


for i in range(23):
    df = pd.read_parquet(
        f"/Users/zhangke/Documents/workspace/58/AIAudio/lerobot/outputs/record/data/chunk-000/episode_0000{str(i).zfill(2)}.parquet")
    print(df.head(1)["index"])
    print(f"length:{len(df)}")

# df = pd.read_parquet("/Users/zhangke/Documents/workspace/58/AIAudio/lerobot/outputs/record/data/chunk-000/episode_000000.parquet")
# start = 0 * 30
# for i in range(df.__len__()):
#     # if df['action'][i][6] != 0:
#     print(f"state:{(i)}, {df['observation.state'][i]}")
#     print(f"action: {df['action'][i]}")

# # 截取前x行数据
# subset_df = df.head(x)
# # 保存为新文件
# new_file_path = '/Users/zhangke/Documents/workspace/58/AIAudio/lerobot/outputs/record/data/chunk-000/episode_000024_head.parquet'

print(df.head())