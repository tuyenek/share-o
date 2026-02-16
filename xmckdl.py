import cloudscraper
import requests
import json
import os
import time
import logging
import re
import uuid
import base64
import random
from datetime import datetime
from tabulate import tabulate
from urllib.parse import urlparse, parse_qs


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
    
    print(f"{Col.RED}   >> Tool By AnhTuyenDZ - Version 1.0.0 <<   {Col.RESET}")
    print(f"{Col.YELLOW}   ──────────────────────────────────────────────────────   {Col.RESET}")

# ==============================================================================
# CẤU HÌNH TOOL
# ==============================================================================
DEBUG = False  # Tắt debug cho đỡ rối mắt, chỉ hiện log cần thiết
TOKEN_FILE = 'token.json'
COOKIE_FB_FILE = 'cookie_fb.json'

# Cấu hình Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Khởi tạo Cloudscraper
scraper = cloudscraper.create_scraper()

# ==============================================================================
# PHẦN 1: CÁC HÀM HỖ TRỢ (UTILS)
# ==============================================================================

def debug_print(text):
    if DEBUG:
        print(f"\033[93m [DEBUG] {text}\033[0m")

def prints(r, g, b, text, end='\n'):
    print(f"\033[38;2;{r};{g};{b}m{text}\033[0m", end=end)

def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def load_json(filename):
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except: return None
    return None

def encode_to_base64(text):
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')

def to_requests_proxies(proxy_str):
    if not proxy_str: return None
    return {'http': proxy_str, 'https': proxy_str}

# ==============================================================================
# PHẦN 2: CÁC HÀM XỬ LÝ FACEBOOK (LOGIN & GRAPHQL)
# ==============================================================================

def facebook_info(cookie: str, proxy: str = None, timeout: int = 15):
    try:
        session = requests.Session()
        if proxy:
            session.proxies = to_requests_proxies(proxy)
        
        session_id = str(uuid.uuid4())
        fb_dtsg = ""
        jazoest = ""
        lsd = ""
        name = ""
        
        # --- LOGIC CHECK i_user (PAGE PROFILE) ---
        try:
            if "i_user=" in cookie:
                # Nếu có i_user, đây là cookie page profile
                user_id = cookie.split("i_user=")[1].split(";")[0]
            elif "c_user=" in cookie:
                # Nếu không có i_user, lấy c_user như bình thường
                user_id = cookie.split("c_user=")[1].split(";")[0]
            else:
                return {'success': False}
        except:
            # print("\033[91m [!] Cookie lỗi: Không tìm thấy ID (c_user/i_user).\033[0m")
            return {'success': False}
        # ----------------------------------------------------------

        headers = {
            "authority": "www.facebook.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "vi",
            "sec-ch-prefers-color-scheme": "light",
            "sec-ch-ua": '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
            "viewport-width": "1366",
            "Cookie": cookie
        }

        # Truy cập trang cá nhân để lấy token
        try:
            url_profile = session.get(f"https://www.facebook.com/{user_id}", headers=headers, timeout=timeout).url
            response = session.get(url_profile, headers=headers, timeout=timeout).text
        except Exception as e:
            # print(f"\033[91m [!] Lỗi kết nối Facebook: {e}\033[0m")
            return {'success': False}

        fb_token = re.findall(r'\["DTSGInitialData",\[\],\{"token":"(.*?)"\}', response)
        if fb_token: fb_dtsg = fb_token[0]

        jazo = re.findall(r'jazoest=(.*?)\"', response)
        if jazo: jazoest = jazo[0]

        lsd_match = re.findall(r'"LSD",\[\],\{"token":"(.*?)"\}', response)
        if lsd_match: lsd = lsd_match[0]

        # --- LOGIC LẤY TÊN (MỚI THÊM) ---
        try:
            # Cách 1: Lấy từ JSON dữ liệu (Chính xác nhất)
            data_split = response.split('"CurrentUserInitialData",[],{')
            if len(data_split) > 1:
                json_data_raw = "{" + data_split[1].split("},")[0] + "}"
                parsed_data = json.loads(json_data_raw)
                name = parsed_data.get("NAME", "")
        except: pass

        if not name:
            try:
                # Cách 2: Lấy từ biến NAME trong source
                _sea = response.split(',"NAME":"')[1].split('",')[0]
                name = bytes(_sea, "utf-8").decode("unicode_escape")
            except: pass

        if not name:
            try:
                # Cách 3: Lấy từ thẻ Title (Dự phòng cuối cùng)
                title = re.search(r'<title>(.*?)</title>', response)
                name = title.group(1) if title else "Facebook User"
            except:
                name = "Facebook User"
        # --------------------------------

        if "828281030927956" in response:
            # print("\033[91m [!] Tài khoản bị Checkpoint 956.\033[0m")
            return {'success': False, 'msg': 'Checkpoint 956'}
        if "1501092823525282" in response:
            # print("\033[91m [!] Tài khoản bị Checkpoint 282.\033[0m")
            return {'success': False, 'msg': 'Checkpoint 282'}

        if not fb_dtsg:
            return {'success': False}

        return {
            'success': True,
            'user_id': user_id,
            'fb_dtsg': fb_dtsg,
            'jazoest': jazoest,
            'lsd': lsd,
            'name': name,
            'session': session,
            'session_id': session_id,
            'cookie': cookie,
            'headers': headers
        }

    except Exception as e:
        # print(f"[Facebook.info] Error: {e}")
        return {'success': False}
def _parse_graphql_response(response):
    try:
        response_json = response.json()
        
        if 'errors' in response_json:
            error = response_json['errors'][0]
            error_msg = error.get('message', '').lower()
            
            if 'login required' in error_msg or 'session has expired' in error_msg:
                return {'status': 'cookie_dead', 'message': 'Cookie đã hết hạn.'}
            if 'temporarily blocked' in error_msg or 'spam' in error_msg:
                 return {'status': 'action_failed', 'message': 'Hành động bị chặn (Spam).'}
            return {'status': 'action_failed', 'message': f"Lỗi FB: {error.get('message')}"}
        
        if 'data' in response_json:
            return {'status': 'success', 'data': response_json['data']}

        return {'status': 'action_failed', 'message': 'Không có dữ liệu trả về.'}
    except Exception as e:
        return {'status': 'action_failed', 'message': f'Lỗi JSON: {e}'}

def get_post_id(session, cookie, link):
    """
    Hàm này giờ chỉ dùng làm dự phòng.
    """
    try:
        # Nếu link chứa ID trực tiếp (video.php?v=...)
        if "story.php" in link or "video.php" in link:
            parsed = parse_qs(urlparse(link).query)
            if 'story_fbid' in parsed: return {'success': True, 'post_id': parsed['story_fbid'][0]}
            if 'v' in parsed: return {'success': True, 'post_id': parsed['v'][0]}
            if 'id' in parsed: return {'success': True, 'post_id': parsed['id'][0]}
            
        ids = re.findall(r'/(\d{10,})', link)
        if ids:
            return {'success': True, 'post_id': max(ids, key=len)}

        return {'success': False, 'message': 'Không tìm thấy ID'}
    except:
        return {'success': False, 'message': 'Lỗi Link'}

def react_post_graphql(data, object_id, type_react, proxy=None):
    """
    Hàm thả cảm xúc sử dụng GraphQL.
    Sử dụng trực tiếp Object ID.
    """
    # debug_print(f"-> Đang thả {type_react} vào ID: {object_id}")
    
    headers = data['headers'].copy()
    headers.update({
        'content-type': 'application/x-www-form-urlencoded',
        'referer': f'https://www.facebook.com/{object_id}', # Fake referer từ chính bài viết đó
        'x-fb-friendly-name': 'CometUFIFeedbackReactMutation',
        'x-fb-lsd': data['lsd']
    })
    
    react_list = {
        "LIKE": "1635855486666999",
        "LOVE": "1678524932434102",
        "CARE": "613557422527858",
        "HAHA": "115940658764963",
        "WOW": "478547315650144",
        "SAD": "908563459236466",
        "ANGRY": "444813342392137"
    }

    # Tạo Feedback ID
    feedback_raw = f"feedback:{object_id}"
    feedback_id = encode_to_base64(feedback_raw)

    variables = {
        "input": {
            "attribution_id_v2": f"CometSinglePostDialogRoot.react,comet.post.single_dialog,via_cold_start,{int(time.time()*1000)},893597,,,",
            "feedback_id": feedback_id,
            "feedback_reaction_id": react_list.get(type_react.upper(), "1635855486666999"),
            "feedback_source": "OBJECT",
            "is_tracking_encrypted": True,
            "tracking": [],
            "session_id": data['session_id'],
            "actor_id": data['user_id'],
            "client_mutation_id": "1"
        },
        "useDefaultActor": False,
        "__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider": False
    }

    json_data = {
        'av': data['user_id'], 
        '__user': data['user_id'], 
        'fb_dtsg': data['fb_dtsg'],
        'jazoest': data['jazoest'], 
        'lsd': data['lsd'], 
        'fb_api_caller_class': 'RelayModern',
        'fb_api_req_friendly_name': 'CometUFIFeedbackReactMutation',
        'variables': json.dumps(variables),
        'server_timestamps': 'true', 
        'doc_id': '24034997962776771', 
    }
    
    try:
        response = data['session'].post('https://www.facebook.com/api/graphql/', headers=headers, data=json_data, timeout=15)
        return _parse_graphql_response(response)
    except requests.exceptions.RequestException as e:
        return {'status': 'action_failed', 'message': f'Lỗi kết nối: {e}'}

def do_reaction_main(fb_data, target_id, type_react):
    """
    Hàm điều phối:
    - Nhận thẳng target_id từ API job.
    - Không cố gắng phân tích Link nữa để tránh lỗi.
    """
    
    # Ép kiểu về string để chắc chắn
    object_id = str(target_id)
    
    # Gọi hàm thả cảm xúc luôn
    res = react_post_graphql(fb_data, object_id, type_react)
    
    if res['status'] == 'success':
        return True, "Thành công"
    else:
        return False, res.get('message')

# ==============================================================================
# PHẦN 3: CÁC HÀM XỬ LÝ API XSMM
# ==============================================================================

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

# --- SỬA ĐỔI: Thêm tham số silent để ẩn bảng khi cần ---
def get_list_accounts_xsmm(token, silent=False):
    url = "https://xsmm.net/api/taskapi/accounts"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # Chỉ in tiêu đề nếu không silent
    if not silent:
        print("\n" + " DANH SÁCH TÀI KHOẢN XSMM ".center(60, "="))
    
    uid_map = {} 
    try:
        response = scraper.get(url, headers=headers)
        data = response.json()
        accounts_list = data.get("accounts", [])
        if not accounts_list:
            if not silent:
                print(" [!] Chưa có tài khoản nào trên hệ thống.")
            return {}
        
        table_data = []
        for index, acc in enumerate(accounts_list, start=1):
            name = acc.get("name", "N/A")
            uid = str(acc.get("account_id", "N/A"))
            sys_id = acc.get("id")
            is_active = acc.get("is_active")
            if uid != "N/A" and sys_id: uid_map[uid] = sys_id
            status = "✅ Active" if is_active else "❌ Die/Off"
            table_data.append([index, name, uid, status, sys_id])
        
        # Chỉ in bảng nếu không silent
        if not silent:
            print(tabulate(table_data, headers=["STT", "Facebook", "UID", "Trạng thái", "System ID"], tablefmt="grid"))
            
        return uid_map
    except: return {}

def add_account_xsmm_retry(xsmm_token, fb_uid):
    url = "https://xsmm.net/api/taskapi/accounts"
    headers = {"Authorization": f"Bearer {xsmm_token}", "Content-Type": "application/json"}
    payload = {"type": "facebook", "link_account": str(fb_uid)}
    print(f"\n [Adding] Thêm UID {fb_uid} vào hệ thống...")
    for attempt in range(1, 6):
        try:
            response = scraper.post(url, headers=headers, json=payload)
            if response.status_code in [200, 201]:
                print(f"   [OK] Thêm thành công.")
                return True
            time.sleep(1)
        except: return False
    return False

def set_active_account(token, system_id):
    url = f"https://xsmm.net/api/taskapi/accounts/{system_id}/set-active"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    try:
        if scraper.put(url, headers=headers).status_code in [200, 201]:
            # Có thể ẩn dòng này nếu muốn sạch hoàn toàn, hiện tại để lại xác nhận nhỏ
            # print(f" [OK] Đã SET ACTIVE tài khoản {system_id}.") 
            return True
        return False
    except: return False

def submit_task_xsmm(xsmm_token, task_id):
    url = "https://xsmm.net/api/taskapi/tasks/complete"
    headers = {"Authorization": f"Bearer {xsmm_token}", "Content-Type": "application/json"}
    payload = {"type": "facebook_like", "task_id": [task_id]}
    try:
        response = scraper.post(url, headers=headers, json=payload)
        if response.status_code in [200, 201]:
            return True
        return False
    except: return False

# ==============================================================================
# PHẦN 4: VÒNG LẶP CHÍNH (MAIN LOOP) CẬP NHẬT ROTATE COOKIE
# ==============================================================================

def process_jobs_with_rotation(xsmm_token, cookie_list, delay_time, jobs_per_cookie):
    url_get_job = "https://xsmm.net/api/taskapi/tasks?type=facebook_like"
    headers = {"Authorization": f"Bearer {xsmm_token}", "Content-Type": "application/json"}
    
    # --- SỬA ĐỔI: Hiện bảng danh sách 1 lần DUY NHẤT ở đây ---
    get_list_accounts_xsmm(xsmm_token, silent=False)
    # -----------------------------------------------------------

    print("\n" + " BẮT ĐẦU CHẠY JOB (MULTI-COOKIE MODE) ".center(60, "="))
    
    job_done_total = 0
    consecutive_errors = 0
    MAX_ERRORS = 15
    cookie_index = 0
    
    while True:
        # Lấy cookie hiện tại
        current_cookie = cookie_list[cookie_index % len(cookie_list)]
        
        # --- SỬA ĐỔI: Ẩn log đổi cookie rườm rà, để hiện log gọn ở dưới ---
        # print(f"\n{Col.BLUE} [Change] Đang sử dụng Cookie {cookie_index % len(cookie_list) + 1}/{len(cookie_list)} {Col.RESET}")
        
        # Đăng nhập FB
        fb_data = facebook_info(current_cookie)
        if not fb_data['success']:
            print(f"{Col.RED} [X] Cookie {cookie_index + 1} die/checkpoint. Chuyển cookie... {Col.RESET}")
            cookie_index += 1
            if cookie_index >= len(cookie_list) * 2: # Tránh lặp vô hạn nếu die hết
                print(" [STOP] Tất cả cookie đều không khả dụng.")
                break
            continue

        # Active account trên XSMM
        # --- SỬA ĐỔI: Gọi hàm với silent=True để không hiện lại bảng ---
        uid_map = get_list_accounts_xsmm(xsmm_token, silent=True)
        # ---------------------------------------------------------------
        
        uid = str(fb_data['user_id'])
        system_id = uid_map.get(uid)
        
        if not system_id:
            if add_account_xsmm_retry(xsmm_token, uid):
                uid_map = get_list_accounts_xsmm(xsmm_token, silent=True)
                system_id = uid_map.get(uid)
        
        if not system_id or not set_active_account(xsmm_token, system_id):
            print(f"{Col.RED} [X] Không thể kích hoạt account {uid} trên XSMM. Chuyển cookie...{Col.RESET}")
            cookie_index += 1
            continue

        # --- SỬA ĐỔI: LOG GỌN THEO YÊU CẦU ---
        print(f"{Col.GREEN} [RUN] Đang chạy nick {uid} : {fb_data['name']} {Col.RESET}")
        # -------------------------------------
        
        jobs_done_this_cookie = 0
        while jobs_done_this_cookie < jobs_per_cookie:
            if consecutive_errors >= MAX_ERRORS:
                print(f"\n\033[91m [STOP] Dừng tool vì lỗi {MAX_ERRORS} job liên tiếp.\033[0m")
                return

            try:
                response = scraper.get(url_get_job, headers=headers)
                if response.status_code == 200:
                    jobs = response.json()
                    
                    if isinstance(jobs, dict):
                        msg = jobs.get('message') or jobs.get('error') or jobs.get('msg')
                        print(f" [Wait] Server báo: {msg} (Nghỉ 10s)", end="\r")
                        time.sleep(10)
                        continue
                    
                    if isinstance(jobs, list) and not jobs:
                        print(" [Wait] Hết nhiệm vụ, nghỉ 10s...        ", end="\r")
                        time.sleep(10)
                        continue
                    
                    if isinstance(jobs, list):
                        for job in jobs:
                            if jobs_done_this_cookie >= jobs_per_cookie: break
                            if consecutive_errors >= MAX_ERRORS: break
                            
                            task_id = job.get("id")
                            target_id = job.get("target_id")
                            reaction = job.get("reaction_type", "LIKE") 
                            points = job.get("points", 0)

                            is_success, msg = do_reaction_main(fb_data, target_id, reaction)
                            
                            if is_success:
                                if submit_task_xsmm(xsmm_token, task_id):
                                    job_done_total += 1
                                    jobs_done_this_cookie += 1
                                    consecutive_errors = 0 
                                    
                                    current_bal = get_user_balance(xsmm_token, silent=True)
                                    timestamp = datetime.now().strftime("%H:%M:%S")
                                    
                                    log = f"Job {job_done_total} | {timestamp} | {reaction} | +{points} Xu | Tổng: {current_bal:,} Xu"
                                    print(f"\033[92m{log}\033[0m") 
                                    
                                    for i in range(delay_time, 0, -1):
                                        print(f" [Delay] Nghỉ {i}s...   ", end="\r")
                                        time.sleep(1)
                                else:
                                    consecutive_errors += 1
                                    print(f"\033[91m [X] Lỗi nhận xu XSMM. ({consecutive_errors}/{MAX_ERRORS})\033[0m")
                            else:
                                consecutive_errors += 1
                                print(f"\033[91m [X] Lỗi FB: {msg} (ID: {target_id}) ({consecutive_errors}/{MAX_ERRORS})\033[0m")
                                if "session" in msg.lower() or "checkpoint" in msg.lower():
                                    jobs_done_this_cookie = jobs_per_cookie # Force switch
                                    break
                                time.sleep(2)
                    else:
                        time.sleep(5)
                else:
                    time.sleep(5)
            except KeyboardInterrupt:
                print("\n [STOP] Đã dừng tool.")
                return
            except Exception as e:
                print(f" [Err] Lỗi: {e}")
                time.sleep(5)
        
        # Hết số job quy định hoặc cookie lỗi -> đổi sang cookie tiếp theo
        cookie_index += 1

# ==============================================================================
# PHẦN 5: MAIN
# ==============================================================================

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner()
    
    # 1. Login XSMM
    token_xsmm = load_json(TOKEN_FILE)
    if not token_xsmm: 
        token_xsmm = input(" [+] Nhập Access Token XSMM: ").strip()
        save_json(TOKEN_FILE, {"access_token": token_xsmm})
    else:
        token_xsmm = token_xsmm.get("access_token")

    if not get_user_balance(token_xsmm):
        print(" [X] Token XSMM không hợp lệ.")
        if os.path.exists(TOKEN_FILE): os.remove(TOKEN_FILE)
        return

    # 2. Nhập file Cookie
    print("\n" + " CẤU HÌNH DANH SÁCH COOKIE ".center(60, "="))
    while True:
        file_path = input(" [+] Nhập tên file chứa danh sách cookie (vd: cookie.txt): ").strip()
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                cookie_list = [line.strip() for line in f if line.strip()]
            if cookie_list:
                print(f" [OK] Đã tìm thấy {len(cookie_list)} cookie.")
                break
            else:
                print(" [!] File trống. Vui lòng kiểm tra lại.")
        else:
            print(" [!] File không tồn tại.")

    # 3. Cấu hình thông số
    try:
        delay = int(input(" [+] Nhập thời gian nghỉ sau mỗi job (giây): "))
    except: delay = 10
    
    try:
        jobs_per_cookie = int(input(" [+] Sau bao nhiêu job thì đổi cookie? : "))
    except: jobs_per_cookie = 10

    # Chạy vòng lặp
    process_jobs_with_rotation(token_xsmm, cookie_list, delay, jobs_per_cookie)

if __name__ == "__main__":
    main()
