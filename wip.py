import requests
import time
import pandas as pd

# Step 1: 登录获取 Token
def login_and_get_token():
    login_url = "http://36.133.174.185:8081/pws/sys/customLogin"
    login_data = {
        "username": "314",         # 替换为你的用户名
        "password": "68241373",    # 替换为你的密码
        "remember_me": True
    }
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Accept": "application/json, text/plain, */*",
        "Tenant-Id": "0"
    }
    session = requests.Session()
    response = session.post(login_url, json=login_data, headers=headers)
    
    if response.status_code == 200:
        response_json = response.json()
        if "result" in response_json and "token" in response_json["result"]:
            token = response_json["result"]["token"]
            print("登录成功，Token:", token)
            return session, token
        else:
            print("登录响应中未找到 Token:", response_json)
            return None, None
    else:
        print("登录失败，状态码：", response.status_code)
        print("响应内容：", response.text)
        return None, None

# Step 2: 使用 Token 请求数据
def request_data(session, token):
    data_url = ("http://36.133.174.185:8081/pws/web/webMesCardWip/list"
                "?_t=1734846903&field=id,,,cardCode,packageCode,pmodel,currentqty,"
                "stepName,arriveTimestamp,waferModel,waferBatch,workOrderCode,startDate,"
                "manufaturingType_dictText,priority_dictText,customerSoCode,customerCode"
                "&pageNo=1&pageSize=10000")
    
    # 获取当前时间戳
    current_timestamp = int(time.time() * 1000)

    # 添加正确的 Headers，包括 X-Access-Token
    headers = {
        "X-Access-Token": token,
        "Content-Type": "application/json;charset=UTF-8",
        "Accept": "application/json, text/plain, */*",
        "Tenant-Id": "0",
        "Origin": "http://36.133.174.185:8008",
        "Referer": "http://36.133.174.185:8008/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "X-Timestamp": str(current_timestamp)
    }
    
    # 发送数据请求
    response = session.get(data_url, headers=headers)
    
    if response.status_code == 200:
        print("数据获取成功！")
        data = response.json()
        records_data = data['result']['records']
        # 使用DataFrame函数将数据转换为DataFrame
        df = pd.DataFrame(records_data)
        # 进行后续的操作
        # 获取大概交期
    else:
        print("数据请求失败，状态码：", response.status_code)
        print("响应内容：", response.text)

# 主函数
if __name__ == "__main__":
    session, token = login_and_get_token()
    
    if token:
        request_data(session, token)
    else:
        print("无法继续请求数据，登录失败或未获取到 Token。")
