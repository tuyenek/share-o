import cloudscraper
import requests
import json
import os
import time
import logging
from datetime import datetime
from tabulate import tabulate

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

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Dùng f-string và r""" để giữ nguyên định dạng và màu sắc
    print(f"""{Col.CYAN}
    
    ████████╗███╗   ██╗███████╗ ██████╗ 
    ╚══██╔══╝████╗  ██║╚══███╔╝██╔═══██╗
       ██║   ██╔██╗ ██║  ███╔╝ ██║   ██║
       ██║   ██║╚██╗██║ ███╔╝  ██║   ██║
       ██║   ██║ ╚████║███████╗╚██████╔╝
       ╚═╝   ╚═╝  ╚═══╝╚══════╝ ╚═════╝
       
    {Col.RESET}""")
    
    print(f"{Col.RED}   >> Tool By AnhTuyenDZ - Version 2.0 <<   {Col.RESET}")
    print(f"{Col.YELLOW}   ──────────────────────────────────────   {Col.RESET}")

# Cấu hình Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

TOKEN_FILE = 'token.json'
TOKEN_FB_FILE = 'token_fb.json'

# Khởi tạo Cloudscraper (Chỉ dùng cho XSMM)
scraper = cloudscraper.create_scraper()

# --- 1. CÁC HÀM HỖ TRỢ FILE ---
def save_token(token):
    with open(TOKEN_FILE, 'w', encoding='utf-8') as f:
        json.dump({"access_token": token}, f, indent=4)

def load_token():
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
                return json.load(f).get("access_token")
        except: return None
    return None

def save_fb_token(token, name, uid):
    data = {"facebook_token": token, "name": name, "uid": uid}
    with open(TOKEN_FB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def load_fb_token():
    if os.path.exists(TOKEN_FB_FILE):
        try:
            with open(TOKEN_FB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except: return None
    return None

# --- 2. CÁC HÀM API XSMM ---
def get_user_balance(token, silent=False):
    url = "https://xsmm.net/api/taskapi/user"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    try:
        response = scraper.get(url, headers=headers)
        if response.status_code == 200:
            user = response.json().get('user', {})
            points = user.get('points', 0)
            if not silent:
                print("\n" + " THÔNG TIN NGƯỜI DÙNG ".center(60, "="))
                print(f" User: {user.get('username')} | Số dư: {points:,} Xu")
            return points
        return 0
    except: return 0

def get_list_accounts_xsmm(token):
    url = "https://xsmm.net/api/taskapi/accounts"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    print("\n" + " DANH SÁCH TÀI KHOẢN TRÊN XSMM ".center(60, "="))
    uid_map = {} 
    try:
        response = scraper.get(url, headers=headers)
        data = response.json()
        accounts_list = data.get("accounts", [])

        if not accounts_list:
            print(" [!] Chưa có tài khoản nào trên hệ thống.")
            return {}

        table_data = []
        for index, acc in enumerate(accounts_list, start=1):
            name = acc.get("name", "N/A")
            uid = str(acc.get("account_id", "N/A"))
            sys_id = acc.get("id")
            is_active = acc.get("is_active")
            
            if uid != "N/A" and sys_id:
                uid_map[uid] = sys_id

            status = "✅ Active" if is_active else "❌ Die/Off"
            table_data.append([index, name, uid, status, sys_id])

        print(tabulate(table_data, headers=["STT", "Tên Facebook", "UID", "Trạng thái", "System ID"], tablefmt="grid"))
        return uid_map
    except Exception as e:
        print(f" [X] Lỗi lấy danh sách: {e}")
        return {}

def add_account_xsmm_retry(xsmm_token, fb_uid):
    url = "https://xsmm.net/api/taskapi/accounts"
    headers = {"Authorization": f"Bearer {xsmm_token}", "Content-Type": "application/json"}
    payload = {"type": "facebook", "link_account": str(fb_uid)}

    print("\n" + f" TIẾN HÀNH THÊM UID: {fb_uid} ".center(60, "="))

    for attempt in range(1, 11):
        try:
            print(f" [Lần thử {attempt}/10] Đang gửi yêu cầu thêm...")
            response = scraper.post(url, headers=headers, json=payload)
            if response.status_code in [200, 201]:
                print(f"   [SUCCESS] Thêm thành công tài khoản!")
                return True
            time.sleep(2)
        except: return False
    return False

def set_active_account(token, system_id):
    url = f"https://xsmm.net/api/taskapi/accounts/{system_id}/set-active"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    print("\n" + f" KÍCH HOẠT TÀI KHOẢN ID: {system_id} ".center(60, "="))
    try:
        response = scraper.put(url, headers=headers)
        if response.status_code in [200, 201]:
            print(f" [OK] Đã SET ACTIVE thành công!")
            return True
        else:
            print(f" [FAIL] Lỗi kích hoạt. HTTP {response.status_code}")
            return False
    except: return False

# --- 3. CÁC HÀM XỬ LÝ JOB ---

def fb_perform_action(fb_token, target_id, reaction_type, current_uid):
    """
    Thực hiện Like/Reaction bằng thư viện REQUESTS (theo ý bạn).
    Có xử lý ghép UID_TARGETID.
    """
    reaction_type = reaction_type.upper()
    
    # URL mặc định cho LIKE
    url = f'https://graph.facebook.com/{target_id}/likes'
    params = {'access_token': fb_token}
    
    # Nếu là cảm xúc khác (LOVE, HAHA...)
    if reaction_type != 'LIKE':
        # Logic ghép UID nếu target_id chưa có
        if "_" not in str(target_id):
            final_id = f"{current_uid}_{target_id}"
        else:
            final_id = target_id
            
        url = f'https://graph.facebook.com/{final_id}/reactions'
        params['type'] = reaction_type

    try:
        # Dùng requests thuần (Ko dùng cloudscraper ở đây để tránh lỗi Graph API)
        response = scraper.post(url, params=params, timeout=20)
        
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        return False

def submit_task_xsmm(xsmm_token, task_id):
    url = "https://xsmm.net/api/taskapi/tasks/complete"
    headers = {"Authorization": f"Bearer {xsmm_token}", "Content-Type": "application/json"}
    payload = {
        "type": "facebook_like",
        "task_id": [task_id]
    }
    try:
        response = scraper.post(url, headers=headers, json=payload)
        if response.status_code in [200, 201]:
            return True
        return False
    except: return False

def process_jobs(xsmm_token, fb_token, current_uid, delay_time):
    """
    Vòng lặp chính xử lý job.
    Nhận thêm tham số:
    - current_uid: để ghép ID.
    - delay_time: thời gian nghỉ do người dùng nhập.
    """
    url_get_job = "https://xsmm.net/api/taskapi/tasks?type=facebook_like"
    headers = {"Authorization": f"Bearer {xsmm_token}", "Content-Type": "application/json"}

    print("\n" + " BẮT ĐẦU CHẠY JOB AUTO ".center(60, "="))
    
    job_done_count = 0
    
    # --- BIẾN ĐẾM LỖI LIÊN TIẾP ---
    consecutive_errors = 0
    MAX_ERRORS = 15
    
    while True:
        # Kiểm tra giới hạn lỗi
        if consecutive_errors >= MAX_ERRORS:
            print(f"\n\033[91m [STOP] Đã dừng tool vì lỗi {MAX_ERRORS} job liên tiếp.\033[0m")
            break

        try:
            # 1. Lấy danh sách Job
            response = scraper.get(url_get_job, headers=headers)
            
            if response.status_code == 200:
                jobs = response.json()
                
                if not jobs:
                    print(" [Wait] Đang đợi job mới... (Nghỉ 10s)", end="\r")
                    time.sleep(10)
                    continue
                
                print(f"\n [INFO] Tìm thấy {len(jobs)} nhiệm vụ. Bắt đầu làm...")

                # 2. Duyệt từng job
                for job in jobs:
                    # Kiểm tra lại ngay trong vòng lặp for
                    if consecutive_errors >= MAX_ERRORS:
                        break

                    task_id = job.get("id")
                    target_id = job.get("target_id")
                    reaction = job.get("reaction_type", "LIKE") 
                    points = job.get("points", 0)

                    # 3. Làm nhiệm vụ Facebook
                    is_success_fb = fb_perform_action(fb_token, target_id, reaction, current_uid)
                    
                    if is_success_fb:
                        # 4. Submit nhận xu
                        if submit_task_xsmm(xsmm_token, task_id):
                            job_done_count += 1
                            
                            # === RESET BỘ ĐẾM LỖI VỀ 0 NẾU THÀNH CÔNG ===
                            consecutive_errors = 0 
                            
                            current_bal = get_user_balance(xsmm_token, silent=True)
                            
                            timestamp = datetime.now().strftime("%H:%M:%S")
                            log = f"Job {job_done_count} | {timestamp} | {reaction} | +{points} Xu | Tổng: {current_bal:,} Xu"
                            print(f"\033[92m{log}\033[0m") 
                            
                            # Delay theo thời gian người dùng nhập
                            for i in range(delay_time, 0, -1):
                                print(f" [Delay] Nghỉ {i}s...   ", end="\r")
                                time.sleep(1)
                        else:
                            # Lỗi Submit XSMM -> Tăng bộ đếm lỗi
                            consecutive_errors += 1
                            print(f"\033[91m [X] Lỗi nhận xu XSMM. (Lỗi liên tiếp: {consecutive_errors}/{MAX_ERRORS})\033[0m")
                    else:
                        # Lỗi Facebook -> Tăng bộ đếm lỗi
                        consecutive_errors += 1
                        print(f"\033[91m [X] Lỗi thả {reaction} Facebook. (Lỗi liên tiếp: {consecutive_errors}/{MAX_ERRORS})\033[0m")
                        time.sleep(2) # Nghỉ nhẹ 2s khi lỗi
            else:
                print(f" [API] Lỗi lấy job: HTTP {response.status_code}")
                time.sleep(5)

        except KeyboardInterrupt:
            print("\n [STOP] Đã dừng tool theo yêu cầu.")
            break
        except Exception as e:
            print(f" [Err] Lỗi luồng chính: {e}")
            time.sleep(5)

# --- 4. HÀM CHECK TOKEN FB ---
def check_fb_token_info(token):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'}
    try:
        url = f'https://graph.facebook.com/me?access_token={token}'
        response = requests.get(url, headers=headers, timeout=20).json()
        
        if 'error' in response: return False
        return response.get('name'), str(response.get('id'))
    except: return False

# --- 5. CHƯƠNG TRÌNH CHÍNH ---
def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner()
    # 1. Login XSMM
    token_xsmm = load_token()
    if not token_xsmm:
        token_xsmm = input(" [+] Nhập Access Token XSMM: ").strip()
        save_token(token_xsmm)
    if not get_user_balance(token_xsmm):
        print(" [X] Token XSMM lỗi.")
        return

    # 2. Check TK & Login FB
    uid_map = get_list_accounts_xsmm(token_xsmm)
    
    saved_fb = load_fb_token()
    token_fb = ""
    print("\n" + " CẤU HÌNH TÀI KHOẢN ".center(60, "="))
    
    if saved_fb:
        print(f" [Gợi ý] Tài khoản cũ: {saved_fb.get('name')} ({saved_fb.get('uid')})")
        use_old = input(f" [?] Bạn có muốn dùng lại không? (y/n): ").lower()
        if use_old == 'y': token_fb = saved_fb.get('facebook_token')

    if not token_fb:
        token_fb = input(" [+] Nhập Token Facebook Mới: ").strip()

    fb_info = check_fb_token_info(token_fb)

    if fb_info:
        name, uid = fb_info
        print(f" [OK] Facebook Live: {name} | UID: {uid}")
        save_fb_token(token_fb, name, uid)
        
        system_id = None
        if uid in uid_map:
            print(f" [SKIP] Tài khoản đã có trên hệ thống.")
            system_id = uid_map[uid]
        else:
            if add_account_xsmm_retry(token_xsmm, uid):
                new_map = get_list_accounts_xsmm(token_xsmm)
                system_id = new_map.get(uid)
        
        if system_id:
            if set_active_account(token_xsmm, system_id):
                
                # --- NHẬP DELAY TỪ BÀN PHÍM ---
                print("\n" + " CẤU HÌNH CHẠY JOB ".center(60, "="))
                try:
                    delay_input = int(input(" [+] Nhập thời gian nghỉ (giây) sau mỗi job: "))
                except:
                    delay_input = 5 # Mặc định nếu nhập sai
                    print(" [!] Nhập sai, lấy mặc định 5 giây.")

                # Chạy job (Truyền thêm delay_input)
                process_jobs(token_xsmm, token_fb, uid, delay_input)
        else:
            print(" [ERR] Không tìm thấy System ID.")
    else:
        print(" [DIE] Token Facebook không hợp lệ.")

if __name__ == "__main__":
    main()
