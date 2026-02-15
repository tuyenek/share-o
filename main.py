import os
import requests
import time
import sys
import random
import string
import json
import base64
import hashlib
import subprocess
import urllib3
from datetime import datetime

# --- [BẮT BUỘC] CẤU HÌNH ĐỂ KHÔNG BỊ LỖI CHỮ TIẾNG VIỆT TRÊN WINDOWS ---
if os.name == 'nt':
    # Ép CMD của Windows chuyển sang bảng mã UTF-8 (65001)
    os.system('chcp 65001 >nul') 
    # Ép Python xuất dữ liệu ra màn hình theo chuẩn UTF-8
    sys.stdout.reconfigure(encoding='utf-8') 

# Tắt cảnh báo SSL cho hosting miễn phí
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CẤU HÌNH MÀU SẮC (GIỮ NGUYÊN THEO FILE CỦA BẠN) ---
class Col:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

# --- HÀM LẤY IP ---
def get_ip():
    try:
        # Lấy IP public hiện tại của người dùng
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        return response.json().get("ip")
    except:
        return "Đang kiểm tra..."

# --- HÀM BANNER (ĐÃ FIX KÝ TỰ KHUNG) ---
def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Col.RED} © Bản Quyền AnhTuyenDz{Col.RESET}")
    print("")
    # Sử dụng ký tự khối chuẩn để tránh vỡ font trên Bitbucket
    print(f"{Col.CYAN}        ████████╗███╗   ██╗███████╗ ██████╗ ")
    print(f"        ╚══██╔══╝████╗  ██║╚══███╔╝██╔═══██╗")
    print(f"           ██║   ██╔██╗ ██║  ███╔╝ ██║   ██║")
    print(f"           ██║   ██║╚██╗██║ ███╔╝  ██║   ██║")
    print(f"           ██║   ██║ ╚████║███████╗╚██████╔╝")
    print(f"           ╚═╝   ╚═╝  ╚═══╝╚══════╝ ╚═════╝ {Col.RESET}")
    print(f"{Col.CYAN}------------------------------------------------------------{Col.RESET}")

# --- HÀM MAIN CHÍNH ---
def main():
    current_ip = get_ip()
    banner()

    # --- PHẦN THÔNG TIN LIÊN HỆ ---
    print(f"{Col.RED}[</>]{Col.RESET} => {Col.YELLOW}Admin:{Col.RESET}       {Col.GREEN}Minh Tuyên{Col.RESET}")
    print(f"{Col.RED}[</>]{Col.RESET} => {Col.YELLOW}MB Bank:{Col.RESET}    {Col.WHITE}0379956051{Col.RESET}")
    print(f"{Col.RED}[</>]{Col.RESET} => {Col.YELLOW}Facebook:{Col.RESET}   {Col.WHITE}Chưa có{Col.RESET}")
    print(f"{Col.RED}[</>]{Col.RESET} => {Col.YELLOW}Zalo:{Col.RESET}       {Col.WHITE}Chưa có{Col.RESET}")
    print(f"{Col.CYAN}------------------------------------------------------------{Col.RESET}")

    # --- PHẦN THÔNG TIN MÁY CHỦ (SỬ DỤNG KHUNG AN TOÀN) ---
    print(f"{Col.CYAN}╔═══════════════════════════════╗")
    print(f"║       Thông Tin Máy Chủ       ║")
    print(f"╚═══════════════════════════════╝{Col.RESET}")
    print(f"{Col.RED}[</>]{Col.RESET} => {Col.YELLOW}Phiên Bản:{Col.RESET}  {Col.GREEN}1.0.1")
    print(f"{Col.RED}[</>]{Col.RESET} => {Col.YELLOW}IP Của Bạn:{Col.RESET} {Col.GREEN}{current_ip}{Col.RESET}")
    print(f"{Col.CYAN}------------------------------------------------------------{Col.RESET}")

    # --- PHẦN MENU TOOL ---
    print(f"{Col.CYAN}╔═══════════════════════════════╗")
    print(f"║       Tool facebook           ║")
    print(f"╚═══════════════════════════════╝{Col.RESET}")
    print(f"{Col.RED}[</>]{Col.RESET} => {Col.YELLOW}Nhập [1.1] Để Chọn Chế Độ Facebook")
    print(f"{Col.RED}[</>]{Col.RESET} => {Col.YELLOW}Nhập [1.2] Để Chọn Chế Độ Facebook đa cookie")
    print(f"{Col.RED}[</>]{Col.RESET} => {Col.YELLOW}Nhập [1.3] Để Chọn Chế Độ Facebook token{Col.RESET}")

    while True:
        try:
            choice = input(f"\n{Col.RED}[</>]{Col.RESET} => {Col.YELLOW}Nhập Lựa Chọn: {Col.RESET}")
            if choice == "1.1":
                print(f"\n{Col.GREEN}>> Đang Vào tool...{Col.RESET}")
                xmckdl = "https://raw.githubusercontent.com/tuyenek/share-o/refs/heads/main/xmckdl.py"
                xm1 = requests.get(xmckdl)
                exec(xm1)
                
                time.sleep(1)
                # Chèn code tool Facebook 1.1 của bạn vào đây
                break
            elif choice in ["1.2", "1.3"]:
                print(f"{Col.YELLOW}>> Chế độ này đang phát triển...{Col.RESET}")
            else:
                print(f"{Col.RED}>> Lựa chọn không hợp lệ!{Col.RESET}")
        except KeyboardInterrupt:
            print(f"\n{Col.RED}>> Đã thoát tool.{Col.RESET}")
            break

if __name__ == "__main__":
    main()
