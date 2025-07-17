import requests
import threading
import time
import sys
import os
from pystyle import Write, Colors
gome_token = []

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    Write.Print(r'''

  _   _ __  __     _____                       
 | | | |  \/  |   |_   _|   _ _   _  ___ _ __  
 | |_| | |\/| |_____| || | | | | | |/ _ \ '_ \ 
 |  _  | |  | |_____| || |_| | |_| |  __/ | | |
 |_| |_|_|  |_|     |_| \__,_|\__, |\___|_| |_|
                              |___/            

                                                       
''', Colors.DynamicMIX((Colors.blue, Colors.purple, Colors.cyan)), interval=0.001)

    Write.Print("-" * 70 + "\n", Colors.white, interval=0.001)
    Write.Print("[+] Tool By Minh Tuyên-TuyenNzo\n", Colors.DynamicMIX((Colors.blue, Colors.purple, Colors.cyan)), interval=0.001)
    Write.Print("[+] Zalo: 0379956051\n", Colors.DynamicMIX((Colors.blue, Colors.purple, Colors.cyan)), interval=0.001)
    Write.Print("[+] Youtube: https://www.youtube.com/@xxxxxxxx\n", Colors.DynamicMIX((Colors.blue, Colors.purple, Colors.cyan)), interval=0.001)
    Write.Print("-" * 70 + "\n", Colors.white, interval=0.001)

def get_token(cookies):
    for cookie in cookies:
        headers = {
            'cookie': cookie,
            'user-agent': 'Mozilla/5.0',
        }
        try:
            res = requests.get('https://business.facebook.com/content_management', headers=headers)
            if "EAAG" in res.text:
                token = res.text.split("EAAG")[1].split('"')[0]
                gome_token.append(f"{cookie}|EAAG{token}")
                print(f"[+] Lấy token thành công")
            else:
                print(f"[-] Không lấy được token từ cookie")
        except Exception as e:
            print(f"[!] Lỗi khi lấy token: {e}")
    return gome_token

def share(cookie_token, post_id):
    cookie, token = cookie_token.split('|')
    headers = {
        'cookie': cookie,
        'user-agent': 'Mozilla/5.0'
    }
    try:
        url = f'https://graph.facebook.com/me/feed?link=https://m.facebook.com/{post_id}&published=0&access_token={token}'
        res = requests.post(url, headers=headers)
        result = res.json()

        if "id" in result:
            print(f"\033[1;32m[✔] SHARE THÀNH CÔNG - POST ID: {post_id}\033[0m")
        else:
            error_code = result.get('error', {}).get('code')
            if error_code == 368:
                print("\033[1;31mTài khoản bị block share. Ấn Ctrl + Z để thoát tool\033[0m")
            else:
                message = result.get('error', {}).get('message', 'Không rõ lỗi')
                print(f"\033[1;31m[✘] SHARE THẤT BẠI - {message}\033[0m")
    except Exception as e:
        print(f"[!] Lỗi share: {e}")

def main():
    clear()
    banner()
    
    print("Nhập các cookie (mỗi cookie cách nhau bằng Enter, để trống dòng để kết thúc):")
    cookies = []
    while True:
        c = input("> ")
        if not c.strip():
            break
        cookies.append(c.strip())
    
    if not cookies:
        print("Chưa nhập cookie nào.")
        return
    
    post_id = input("Nhập ID bài viết cần share: ").strip()
    delay = int(input("Delay giữa mỗi share (giây): "))
    count = int(input("Số lần share (tối đa): "))
    
    all_token = get_token(cookies)
    
    if not all_token:
        print("Không lấy được token nào.")
        return
    
    stt = 0
    while stt < count:
        for tk in all_token:
            if stt >= count:
                break
            stt += 1
            threading.Thread(target=share, args=(tk, post_id)).start()
            time.sleep(delay)
    
    gome_token.clear()
    input("Đã chạy xong. Nhấn Enter để thoát.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Bạn đã dừng tool.")
        sys.exit()
