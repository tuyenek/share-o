import requests
import time
import re
import json
import os
from datetime import datetime

API_KEY = "969bac8b8206374b7ee0330a1f3cab47"
API_URL = "https://uplikesub.com/api/v2"
SERVICE_ID = 1855
BUFF_QUANTITY = 500

BUFF_LOG_FILE = "buff_log.json"
DAILY_LIMIT = 5

def load_log():
    if os.path.exists(BUFF_LOG_FILE):
        with open(BUFF_LOG_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except:
                data = {}
    else:
        data = {}
    return data

def save_log(log):
    with open(BUFF_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

def get_today_count(user_key="local_user"):
    log = load_log()
    today = datetime.now().strftime("%Y-%m-%d")
    return len([x for x in log.get(user_key, []) if x["date"] == today])

def can_buff_today(user_key="local_user"):
    return get_today_count(user_key) < DAILY_LIMIT

def add_buff_log(link, user_key="local_user"):
    log = load_log()
    today = datetime.now().strftime("%Y-%m-%d")
    entry = {"link": link, "date": today, "timestamp": int(time.time())}
    if user_key not in log:
        log[user_key] = []
    log[user_key].append(entry)
    save_log(log)

def order_buff_tiktok(link, quantity):
    payload = {
        "key": API_KEY,
        "action": "add",
        "service": SERVICE_ID,
        "link": link,
        "quantity": quantity
    }
    try:
        response = requests.post(API_URL, data=payload, timeout=10)
        data = response.json()
        if "order" in data:
            print('buff view thành công')
            return True
    except:
        pass
    print("Đã xảy ra lỗi! Vui lòng thử lại hoặc kiểm tra lại link, số lượt buff trong ngày, số dư hoặc hệ thống.")
    return False

def is_valid_tiktok_link(link):
    pattern = r"^https:\/\/www\.tiktok\.com\/@[\w\.-]+\/video\/\d+"
    return re.match(pattern, link)

if __name__ == "__main__":
    today_used = get_today_count()
    remaining = DAILY_LIMIT - today_used
    print(f"Bạn còn {remaining}/{DAILY_LIMIT} lượt buff view trong ngày.")
    if not can_buff_today():
        print(f"Bạn đã dùng hết {DAILY_LIMIT}/{DAILY_LIMIT} lượt buff view trong ngày. Vui lòng quay lại vào ngày mai.")
        exit(0)
    link = input("Nhập link cần buff (Định dạng: https://www.tiktok.com/@username/video/23445): ").strip()
    while not is_valid_tiktok_link(link):
        print("Link không đúng định dạng! Vui lòng nhập lại:")
        link = input().strip()
    if order_buff_tiktok(link, BUFF_QUANTITY):
        add_buff_log(link)
