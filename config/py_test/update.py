import requests

def main(conversation_id:str, record_id) -> dict:

    # NocoDB 的 API 密钥
    API_KEY = "njfEQq62RXREk2B0zapebTBIVDwDo0jqQWCidnsr"
    # 表的 API URL
    TABLE_URL = "https://nocodb.58corp.com/api/v2/tables/m42yzorrrnn9psd/records"

    # 要插入的数据
    data = {
        "Id": record_id,
        "materialId": "7",
        "outputType": "video",
        "conversation_id": conversation_id,
        "status": 2
    }

    # 设置请求头，包含 API 密钥
    headers = {
        "xc-token": API_KEY,
        "Content-Type": "application/json"
    }

    try:
        # 发送 POST 请求插入数据
        response = requests.patch(TABLE_URL, json=data, headers=headers)
        print("zk")
        # 检查响应状态码
        if response.status_code == 200 or response.status_code == 204:
            print("数据更新成功！")
            return {
                "db_update":0,
                "result":{
                        "conversation_id": conversation_id,
                        "url" : "",
                        "type":"video",
                        "materialId":"7",
                        "status":2
                    }
                }
    except requests.RequestException as e:
        print(e)

if __name__ == "__main__":
    main("1235", 820)