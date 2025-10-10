import requests
import json

# 替换为你自己的 Dify API 密钥
API_KEY = "app-9l9Dor0ZDd79tvcbSB15f2JT"
# Dify 的文本生成 API 端点
API_URL = "https://dify.58corp.com/v1/chat-messages"

# 请求的数据
data = {
    "inputs": {
        "cateName":"家政"
    },

    "conversation_id":"",
    "user":"wangmingzhong-sse",
    "query":"开始"
}

# 设置请求头
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

try:
    # 发送 POST 请求
    response = requests.post(API_URL, headers=headers, data=json.dumps(data))

    # 检查响应状态码
    if response.status_code == 200:
        res = response.json()
        print(res)
        result = json.loads(res['answer'])['videoUrl']
        print("请求成功，响应内容：")
        print(result)
    else:
        print(f"请求失败，状态码：{response.status_code}，错误信息：{response.text}")
except requests.RequestException as e:
    print(f"请求发生异常：{e}")
