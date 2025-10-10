import json
import random
def format_seconds(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    remaining_seconds = seconds % 60
    return "{:02d}:{:02d}:{:06.3f}".format(hours, minutes, remaining_seconds)

import random


import random

def get_videos(target_duration: float):
    pic_array = [
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609167403-IMG_3820.MOV",
                "duration": 7.77
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609170379-IMG_2594.MOV",
                "duration": 12.64
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609175405-IMG_2595.MOV",
                "duration": 11.89
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609178493-IMG_2591.MOV",
                "duration": 7.64
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609180146-IMG_3842.MOV",
                "duration": 3.72
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609183202-IMG_2592.MOV",
                "duration": 10.78
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609186654-IMG_2593.MOV",
                "duration": 10.39
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609191565-IMG_3864.MOV",
                "duration": 14.71
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609195717-IMG_3865.MOV",
                "duration": 8.77
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609199277-IMG_3866.MOV",
                "duration": 11.91
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609209306-32518_raw.mp4",
                "duration": 43.84
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609215897-IMG_3862.MOV",
                "duration": 16.84
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609218901-32519_raw.mp4",
                "duration": 6.7
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609222650-IMG_3813.MOV",
                "duration": 14.48
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609225828-IMG_3794.MOV",
                "duration": 8.29
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609228017-IMG_3838.MOV",
                "duration": 4.65
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609231779-IMG_3805.MOV",
                "duration": 9.99
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609233615-IMG_3839.MOV",
                "duration": 5.62
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609235708-IMG_3795.MOV",
                "duration": 5.34
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609237013-IMG_1178.MOV",
                "duration": 2.79
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609238555-IMG_3816.MOV",
                "duration": 5.37
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609239452-IMG_1230.MOV",
                "duration": 1.64
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609241612-IMG_3879.MOV",
                "duration": 4.64
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609255420-IMG_1276.MOV",
                "duration": 43.39
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609263877-IMG_3878.MOV",
                "duration": 15.76
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609267380-IMG_3885.MOV",
                "duration": 7.16
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609272896-IMG_3884.MOV",
                "duration": 26.82
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609279226-IMG_3882.MOV",
                "duration": 17.83
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609283410-IMG_3876.MOV",
                "duration": 8.17
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609286710-IMG_3877.MOV",
                "duration": 6.8
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609289985-IMG_3874.MOV",
                "duration": 11.29
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609295163-1806_raw.mp4",
                "duration": 4.63
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609298397-IMG_1178.MOV",
                "duration": 2.79
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609302993-IMG_1262.MOV",
                "duration": 10.41
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609306694-IMG_3887.MOV",
                "duration": 8.19
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609309164-IMG_3844.MOV",
                "duration": 4.24
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609311706-IMG_3846.MOV",
                "duration": 7.39
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609313960-IMG_3843.MOV",
                "duration": 4.99
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609316814-IMG_3894.MOV",
                "duration": 7.79
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609320769-IMG_3895.MOV",
                "duration": 8.82
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609326230-IMG_3897.MOV",
                "duration": 21.33
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609329174-IMG_3896.MOV",
                "duration": 3.9
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609332127-IMG_3888.MOV",
                "duration": 5.7
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609333598-IMG_3801.MOV",
                "duration": 6.84
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609335516-IMG_1178.MOV",
                "duration": 2.79
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609338765-IMG_3802.MOV",
                "duration": 10.51
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609340114-IMG_3803.MOV",
                "duration": 3.82
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609344348-IMG_3886.MOV",
                "duration": 15.63
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609348076-IMG_3850.MOV",
                "duration": 6.49
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609350033-IMG_3857.MOV",
                "duration": 4.05
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609352505-IMG_3881.MOV",
                "duration": 6.17
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609354314-IMG_3856.MOV",
                "duration": 10.16
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609359094-IMG_3858.MOV",
                "duration": 16.39
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609361466-IMG_3859.MOV",
                "duration": 3.7
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609363400-IMG_1282.MOV",
                "duration": 2.94
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609364565-IMG_3861.MOV",
                "duration": 4.34
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609367357-IMG_3849.MOV",
                "duration": 8.31
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609369740-IMG_3848.MOV",
                "duration": 6.34
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609370452-IMG_3860.MOV",
                "duration": 1.48
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609371392-IMG_1194.MOV",
                "duration": 2.57
            },
            {
                "url": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1746609374616-IMG_1193.MOV",
                "duration": 5.48
            }
        ]

    selected = []
    total_duration = 0.0

    # 打乱列表顺序
    random.shuffle(pic_array)

    for item in pic_array:
        selected.append(item)
        total_duration += item["duration"]
        if total_duration > target_duration:
            break
    print(f"total_duration:{total_duration}")
    return selected, total_duration

def main(audioUrl:str, formatDuration:str, str_url:str, audioDuration:float):
    temp_json = '''{
  "profile": {
    "width": 1080,
    "height": 1920,
    "length": "00:00:42.600",
    "inTime": "00:00:00.000",
    "outTime": "00:00:42.600"
  },
  "materials": {
    "videos": [
      {
        "resource": "https://lbgcrm015.58wos.com.cn/MnrjIhGfEMSp/video/dasao1.mov",
        "inTime": "00:00:00.000",
        "outTime": "00:00:09.080",
        "length": "00:00:09.120",
        "type": 0
      },
      {
        "resource": "https://lbgcrm015.58wos.com.cn/MnrjIhGfEMSp/video/dasao1.mov",
        "inTime": "00:00:00.000",
        "outTime": "00:00:09.080",
        "length": "00:00:09.120",
        "type": 0
      },
      {
        "resource": "https://lbgcrm015.58wos.com.cn/MnrjIhGfEMSp/video/dasao.mov",
        "inTime": "00:00:00.000",
        "outTime": "00:00:42.560",
        "length": "00:00:42.600",
        "type": 0
      }
    ],
    "audio": {
      "resource": "https://aiplay017.58wos.com.cn/HioeDcBaHiJN/midjourneyout/1745978439714-dasao.MP3",
      "inTime": "00:00:00.000",
      "outTime": "00:00:42.600",
      "length": "00:00:42.640",
      "type": 2
    }
  },
  "subtitle": {
    "srtUrl": "https://lbgcrm015.58wos.com.cn/MnrjIhGfEMSp/video/dasao.srt"
  }
}'''
    pic_array, total_duration = get_videos(audioDuration)
    result_json = json.loads(temp_json)
    result_json["profile"]["length"] = formatDuration
    result_json["profile"]["outTime"] = formatDuration
    result_json["subtitle"]["srtUrl"] = str_url
    result_json["materials"]["video_duration"] = total_duration
    temp = result_json["materials"]["audio"]
    temp["resource"] = audioUrl
    temp["outTime"] = formatDuration
    temp["length"] = formatDuration
    videos = []
    for index,index_json in enumerate(pic_array):
        length = format_seconds(index_json["duration"])
        item = {
            "resource": index_json["url"],
            "inTime": "00:00:00.000",
            "outTime": length,
            "length": length,
            "type": 0
          }
        videos.append(item)
    result_json["materials"]["videos"] = videos
    print(result_json)
    return { "mtl_data":json.dumps(result_json)}



if __name__ == '__main__':
     #main("test", "conversation_id",26)
    #print(format_seconds(10.3))

     # main("test://", "00:00:12.00", "test2")
     print(get_videos(50))