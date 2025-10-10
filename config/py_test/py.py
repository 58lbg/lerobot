import json

import requests

def main(arg1: str, conversation_id:str, record_id) -> dict:

    # NocoDB 的 API 密钥
    API_KEY = "njfEQq62RXREk2B0zapebTBIVDwDo0jqQWCidnsr"
    # 表的 API URL
    TABLE_URL = "https://nocodb.58corp.com/api/v2/tables/m42yzorrrnn9psd/records"

    # 要插入的数据
    data = {
        # "Id": record_id,
        "materialId": "6",
        "outputStr": arg1,
        "outputType": "video",
        "conversation_id": conversation_id,
        "status": 1
    }

    # 设置请求头，包含 API 密钥
    headers = {
        "xc-token": API_KEY,
        "Content-Type": "application/json"
    }

    try:
        # 发送 POST 请求插入数据
        response = requests.post(TABLE_URL, json=data, headers=headers)
        print("zk")
        # 检查响应状态码
        if response.status_code == 200 or response.status_code == 204:
            tempJson = response.json()
            print("数据更新成功！")
            return { "result":tempJson["Id"]}
    except requests.RequestException as e:
        print(e)

def format_seconds(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    remaining_seconds = seconds % 60
    return "{:02d}:{:02d}:{:06.3f}".format(hours, minutes, remaining_seconds)


def set_mtl_data(pics:str, audioUrl:str, formatDuration:str, str_url:str):
    temp_json = '''{
  "profile": {
    "width": 1080,
    "height": 1920,
    "length": "00:00:10.640",
    "inTime": "00:00:00.000",
    "outTime": "00:00:10.600"
  },
  "materials": {
    "imagesWithoutFilter": [
      {
        "resource": "https://pic4.58cdn.com.cn/nowater/lbgfe/image/n_v3ee5db01168dc43dbb3d7651ea138d479.jpg",
        "inTime": "00:00:00.000",
        "outTime": "03:59:59.960",
        "length": "04:00:00.000",
        "blankLength": "00:00:09.360",
        "entryOutTime": "00:00:01.240"
      },
      {
        "resource": "https://pic4.58cdn.com.cn/nowater/lbgfe/image/n_v3e5f13f719f4e4d048b50a2b679007483.jpg",
        "inTime": "00:00:00.000",
        "outTime": "03:59:59.960",
        "length": "04:00:00.000",
        "blankLength": "00:00:08.560",
        "entryOutTime": "00:00:00.760"
      },
      {
        "resource": "https://pic4.58cdn.com.cn/nowater/lbgfe/image/n_v3ef0d68d6ac984b88830a6491e8f4c533.jpg",
        "inTime": "00:00:00.000",
        "outTime": "03:59:59.960",
        "length": "04:00:00.000",
        "blankLength": "00:00:07.760",
        "entryOutTime": "00:00:00.760"
      },
      {
        "resource": "https://pic4.58cdn.com.cn/nowater/lbgfe/image/n_v38904019311f84b829da0383d719026e0.jpg",
        "inTime": "00:00:00.000",
        "outTime": "03:59:59.960",
        "length": "04:00:00.000",
        "blankLength": "00:00:06.960",
        "entryOutTime": "00:00:00.760"
      },
      {
        "resource": "https://pic4.58cdn.com.cn/nowater/lbgfe/image/n_v34e4239e2e6304abc862e1f216cbcda8f.jpg",
        "inTime": "00:00:00.000",
        "outTime": "03:59:59.960",
        "length": "04:00:00.000",
        "blankLength": "00:00:06.160",
        "entryOutTime": "00:00:00.760"
      },
      {
        "resource": "https://pic4.58cdn.com.cn/nowater/lbgfe/image/n_v31de4e9f25dd44a9f8d142092d932a256.jpg",
        "inTime": "00:00:00.000",
        "outTime": "03:59:59.960",
        "length": "04:00:00.000",
        "blankLength": "00:00:05.360",
        "entryOutTime": "00:00:00.760"
      },
      {
        "resource": "https://pic4.58cdn.com.cn/nowater/lbgfe/image/n_v385a22541e8ee4876ae4f23c5f9ff1446.jpg",
        "inTime": "00:00:00.000",
        "outTime": "03:59:59.960",
        "length": "04:00:00.000",
        "blankLength": "00:00:04.560",
        "entryOutTime": "00:00:00.760"
      },
      {
        "resource": "https://pic4.58cdn.com.cn/nowater/lbgfe/image/n_v3ab6e1640a5b6442d885aff9ce4a1d75a.jpg",
        "inTime": "00:00:00.000",
        "outTime": "03:59:59.960",
        "length": "04:00:00.000",
        "blankLength": "00:00:03.760",
        "entryOutTime": "00:00:00.760"
      },
      {
        "resource": "https://pic4.58cdn.com.cn/nowater/lbgfe/image/n_v375e894e5d6f645a0a863b6126fb0d74d.jpg",
        "inTime": "00:00:00.000",
        "outTime": "03:59:59.960",
        "length": "04:00:00.000",
        "blankLength": "00:00:02.960",
        "entryOutTime": "00:00:00.760"
      }
    ],
    "imagesWithFilter": [
      {
        "resource": "https://pic4.58cdn.com.cn/nowater/lbgfe/image/n_v3ee5db01168dc43dbb3d7651ea138d479.jpg",
        "inTime": "00:00:00.000",
        "outTime": "03:59:59.960",
        "length": "04:00:00.000",
        "blankLength": "00:00:01.920",
        "entryInTime": "00:00:00.000",
        "entryOutTime": "00:00:01.000",
        "filterOutTime": "00:00:01.000",
        "rect": "720 1280 360 640 1"
      },
      {
        "resource": "https://pic4.58cdn.com.cn/nowater/lbgfe/image/n_v3e5f13f719f4e4d048b50a2b679007483.jpg",
        "inTime": "00:00:00.000",
        "outTime": "03:59:59.960",
        "length": "04:00:00.000",
        "blankLength": "00:00:01.680",
        "entryInTime": "00:00:03.000",
        "entryOutTime": "00:00:04.240",
        "filterInTime": "00:00:03.000",
        "filterOutTime": "00:00:04.240",
        "rect": "720 640 360 640 1"
      },
      {
        "resource": "https://pic4.58cdn.com.cn/nowater/lbgfe/image/n_v3ef0d68d6ac984b88830a6491e8f4c533.jpg",
        "inTime": "00:00:00.000",
        "outTime": "03:59:59.960",
        "length": "04:00:00.000",
        "blankLength": "00:00:01.440",
        "entryInTime": "00:00:02.000",
        "entryOutTime": "00:00:03.480",
        "filterInTime": "00:00:02.000",
        "filterOutTime": "00:00:03.480",
        "rect": "720 0 360 640 1"
      },
      {
        "resource": "https://pic4.58cdn.com.cn/nowater/lbgfe/image/n_v38904019311f84b829da0383d719026e0.jpg",
        "inTime": "00:00:00.000",
        "outTime": "03:59:59.960",
        "length": "04:00:00.000",
        "blankLength": "00:00:00.720",
        "entryInTime": "00:00:01.000",
        "entryOutTime": "00:00:03.200",
        "filterInTime": "00:00:01.000",
        "filterOutTime": "00:00:03.200",
        "rect": "359 1280 362 640 1"
      },
      {
        "resource": "https://pic4.58cdn.com.cn/nowater/lbgfe/image/n_v34e4239e2e6304abc862e1f216cbcda8f.jpg",
        "inTime": "00:00:00.000",
        "outTime": "03:59:59.960",
        "length": "04:00:00.000",
        "blankLength": "00:00:00.960",
        "entryInTime": "00:00:00.040",
        "entryOutTime": "00:00:02.000",
        "filterInTime": "00:00:00.040",
        "filterOutTime": "00:00:02.000",
        "rect": "359 640 362 640 1"
      },
      {
        "resource": "https://pic4.58cdn.com.cn/nowater/lbgfe/image/n_v31de4e9f25dd44a9f8d142092d932a256.jpg",
        "inTime": "00:00:00.000",
        "outTime": "03:59:59.960",
        "length": "04:00:00.000",
        "blankLength": "00:00:01.200",
        "entryInTime": "00:00:00.000",
        "entryOutTime": "00:00:01.720",
        "filterOutTime": "00:00:01.720",
        "rect": "359 0 362 640 1"
      },
      {
        "resource": "https://pic4.58cdn.com.cn/nowater/lbgfe/image/n_v385a22541e8ee4876ae4f23c5f9ff1446.jpg",
        "inTime": "00:00:00.000",
        "outTime": "03:59:59.960",
        "length": "04:00:00.000",
        "blankLength": "00:00:00.480",
        "entryInTime": "00:00:00.320",
        "entryOutTime": "00:00:02.760",
        "filterInTime": "00:00:00.320",
        "filterOutTime": "00:00:02.760",
        "rect": "0 1280 360 640 1"
      },
      {
        "resource": "https://pic4.58cdn.com.cn/nowater/lbgfe/image/n_v3ab6e1640a5b6442d885aff9ce4a1d75a.jpg",
        "inTime": "00:00:00.000",
        "outTime": "03:59:59.960",
        "length": "04:00:00.000",
        "blankLength": "00:00:00.240",
        "entryInTime": "00:00:00.000",
        "entryOutTime": "00:00:02.680",
        "filterOutTime": "00:00:02.680",
        "rect": "0 640 360 640 1"
      },
      {
        "resource": "https://pic4.58cdn.com.cn/nowater/lbgfe/image/n_v375e894e5d6f645a0a863b6126fb0d74d.jpg",
        "inTime": "00:00:00.000",
        "outTime": "00:09:59.960",
        "length": "00:10:00.000",
        "blankLength": "00:00:00.000",
        "entryInTime": "00:00:00.000",
        "entryOutTime": "00:00:02.920",
        "filterOutTime": "00:00:02.920",
        "rect": "0 0 360 640 1"
      }
    ],
    "audios": [
      {
        "resource": "https://lbgcrm015.58wos.com.cn/MnrjIhGfEMSp/video/background_music.MP3",
        "inTime": "00:00:00.000",
        "outTime": "00:00:10.600",
        "length": "00:00:10.640",
        "entryInTime": "00:00:00.000",
        "entryOutTime": "00:00:10.600"
      }
    ]
  },
  "subtitle": {
    "srtUrl": "https://lbgcrm015.58wos.com.cn/MnrjIhGfEMSp/video/subtitle.srt"
  }
}'''
    pic_array = json.loads(pics)
    result_json = json.loads(temp_json)
    result_json["profile"]["length"] = formatDuration
    result_json["profile"]["outTime"] = formatDuration
    result_json["subtitle"]["srtUrl"] = str_url
    temp = result_json["materials"]["audios"][0]
    temp["resource"] = audioUrl
    temp["outTime"] = formatDuration
    temp["length"] = formatDuration
    temp["entryOutTime"] = formatDuration
    temp = result_json["materials"]["imagesWithoutFilter"]
    for index,index_json in enumerate(temp):
        index_json["resource"] = pic_array[index]
    temp = result_json["materials"]["imagesWithFilter"]
    for index, index_json in enumerate(temp):
        index_json["resource"] = pic_array[index]
    return result_json



if __name__ == '__main__':
     #main("test", "conversation_id",26)
    #print(format_seconds(10.3))
     array = '''
     [
         "https://pic4.58cdn.com.cn/nowater/lbgfe/image/n_v3ab6e1640a5b6442d885aff9ce4a1d75a.jpg",
         "https://pic4.58cdn.com.cn/nowater/lbgfe/image/n_v375e894e5d6f645a0a863b6126fb0d74d.jpg",
         "https://pic4.58cdn.com.cn/nowater/lbgfe/image/n_v3ab6e1640a5b6442d885aff9ce4a1d75a.jpg",
         "https://pic4.58cdn.com.cn/nowater/lbgfe/image/n_v375e894e5d6f645a0a863b6126fb0d74d.jpg",
         "https://pic4.58cdn.com.cn/nowater/lbgfe/image/n_v3ab6e1640a5b6442d885aff9ce4a1d75a.jpg",
         "https://pic4.58cdn.com.cn/nowater/lbgfe/image/n_v375e894e5d6f645a0a863b6126fb0d74d.jpg",
         "https://pic4.58cdn.com.cn/nowater/lbgfe/image/n_v3ab6e1640a5b6442d885aff9ce4a1d75a.jpg",
         "https://pic4.58cdn.com.cn/nowater/lbgfe/image/n_v375e894e5d6f645a0a863b6126fb0d74d.jpg",
         "https://pic4.58cdn.com.cn/nowater/lbgfe/image/n_v3ab6e1640a5b6442d885aff9ce4a1d75a.jpg"
     ]'''
     set_mtl_data(array, "test://", "00:00:12.00", "test2")