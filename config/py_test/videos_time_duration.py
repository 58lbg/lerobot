import os
import json
import subprocess

from moviepy import VideoFileClip

import requests
# 上传文件到wos
def upload_to_wos(file_path):
    # logger_debug_msg(f'文件开始上传 文件地址: {file_path} ')

    serverUrl = "https://ireview.58corp.com/api/aigc/uploadVideo"
    #print('upload_to_wos: ', file_path);
    with open(file_path, "rb") as f:
        files = {
            "file": f,
        }
        uploadRes = requests.post(serverUrl, files=files)
        #print(uploadRes.text)
        resUploadObj = uploadRes.json()
        #print('resUploadObj', resUploadObj);
        resource_url = resUploadObj['data']['url']
        #print('resource_url', resource_url);
        # logger_debug_msg(f'文件开始结束 网址 resource_url: {resource_url} ')

    return resource_url

def get_duration_ffprobe(file_path):
    try:
        # 获取宽高和时长（json）
        cmd1 = [
            "ffprobe",
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height:format=duration",
            "-of", "json",
            file_path
        ]
        result1 = subprocess.run(cmd1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        info = json.loads(result1.stdout)

        duration = float(info["format"]["duration"])
        stream = info["streams"][0]
        width = stream.get("width")
        height = stream.get("height")

        # 读取原始文本信息来查找 rotate
        cmd2 = [
            "ffprobe",
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream_tags=rotate",
            "-of", "default=noprint_wrappers=1:nokey=1",
            file_path
        ]
        result2 = subprocess.run(cmd2, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        rotation_text = result2.stdout.strip()

        rotation = int(rotation_text) if rotation_text.isdigit() else 0
        # 转换人视角的长宽
        if rotation in [90, 270]:
            width, height = height, width
        elif rotation in [180]:
            # 当旋转180度时，长宽不需要交换
            pass

        duration = round(duration, 2) if duration is not None else None
        return duration, width, height

    except Exception as e:
        print(f"Failed to get video info for {file_path}: {e}")
        return None


def get_video_info_from_dir_ffprobe(dir_path, video_extensions=None):
    if video_extensions is None:
        video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.flv']

    result = []

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in video_extensions:
                full_path = os.path.join(root, file)
                duration, width, height = get_duration_ffprobe(full_path)
                if duration is None:
                    continue
                url = full_path
                if duration is not None and duration > 0:
                    url = upload_to_wos(full_path)

                if url is None:
                    continue
                if duration:
                    result.append({
                        "url": url,
                        "duration": duration
                    })

    return result

def get_video_info(directory):
    video_info_list = []
    # 遍历指定目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 检查文件是否为视频文件
            if file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                file_path = os.path.join(root, file)
                try:
                    # 打开视频文件
                    clip = VideoFileClip(file_path)
                    # 获取视频时长
                    duration = clip.duration
                    clip.close()
                    url = file_path
                    if duration > 0:
                        url = upload_to_wos(file_path)

                    if url is None:
                        continue

                    # 构建视频信息字典
                    video_info = {
                        "url": url,
                        "duration": duration
                    }
                    video_info_list.append(video_info)
                except Exception as e:
                    print(f"Error processing {file}: {e}")
    return video_info_list


if __name__ == "__main__":
    # 指定目录
    directory = '/Volumes/work/下载/分类视频'
    # video_info = get_video_info(directory)
    video_info = get_video_info_from_dir_ffprobe(directory)

    # print(get_duration_ffprobe("/Users/zhangke/Downloads/screen_record_1746443893372.mp4"))
    # 输出 JSON 数组
    print(json.dumps(video_info, indent=4))

    out_txt = '''
    [
    {
        "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746530429217-IMG_1276.MOV",
        "duration": 43.39
    },
    {
        "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746530437915-1806_raw.mp4",
        "duration": 4.63
    },
    {
        "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746530463159-IMG_8941.MOV",
        "duration": 9.99
    },
    {
        "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746530466286-IMG_1178.MOV",
        "duration": 2.79
    }
]
    '''

