from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json

dataLocation = "Your-OnlineJudge-Tracker/data.json"

def load_data():
    try:
        with open(dataLocation, "r", encoding="utf-8") as file:
            data = json.load(file)
            print("成功讀取資料：", data)
            return data
    except FileNotFoundError:
        print("檔案不存在")
        return {"latestProblemID": -1, "semester": "PR113-2-", "problemURL": "http://134.208.3.66/problem/"}


def update_latest_problem_id(data):
    with open(dataLocation, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print("已更新目前最新題號：latestProblemID =", data["problemURL"])

# 使用 Chrome 瀏覽器
driver = webdriver.Chrome()
data = load_data()

while True:
    # 判斷檔案是否可用
    if data["problemURL"] == -1:
        break

    # 目標網址
    url = data["problemURL"] + data["semester"] + str(data["latestProblemID"])

    # 開啟網頁
    driver.get(url)

    # 等待網頁完全加載
    time.sleep(3)

    # 獲取動態加載後的頁面內容
    html = driver.page_source

    # 使用 BeautifulSoup 解析
    soup = BeautifulSoup(html, 'html.parser')

    # 查找目標標籤
    content_tag = soup.find('p', {'class': 'content', 'data-v-6e5e6c6e': ''})

    if content_tag:
        if (len(content_tag.get_text(strip=True)) != 0):
            print("已發布新題目：", data["latestProblemID"])
            data["latestProblemID"] += 1
        else:
            print("完畢！")
            update_latest_problem_id(data)
            break
    else:
        print("尚未發布或無法取得內容")
        break

# 關閉瀏覽器
driver.quit()