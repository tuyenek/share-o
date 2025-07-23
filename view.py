#!/usr/bin/python3
# Tool by Lâm Tilo - Đăng nhập bằng cookie PHPSESSID

import os
import threading, requests, ctypes, random, json, time, base64, re
from prettytable import PrettyTable
from urllib.parse import unquote, urlparse
from string import ascii_letters, digits
from time import strftime
from colorama import init, Fore

init(autoreset=True)

class Zefoy:
    def __init__(self):
        self.base_url = 'https://zefoy.com/'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
        }
        self.session = requests.Session()
        self.service = 'Views'
        self.services = {}
        self.services_ids = {}
        self.services_status = {}
        self.text = 'LÂM TILO'
        self.video_key = None
        self.video_info = None

        cookie_input = input("[LÂMTILO]</> Dán toàn bộ chuỗi cookie từ trình duyệt Zefoy.com: ").strip()
		match = re.search(r'PHPSESSID=([^;]+)', cookie_input)
		if match:
			phpsessid = match.group(1)
			self.session.cookies.set("PHPSESSID", phpsessid, domain='zefoy.com')
			print(f"[LÂMTILO] Sử dụng PHPSESSID: {phpsessid}")
		else:
			print("[LÂMTILO] ❌ Không tìm thấy PHPSESSID trong chuỗi cookie.")
			exit(1)


        url1 = input("[LÂMTILO]</> Nhập link video TikTok: ")
        self.url = url1

    def send_cookie_login(self):
        request = self.session.get(self.base_url, headers=self.headers)
        if 'Enter Video URL' in request.text:
            self.video_key = request.text.split('" placeholder="Enter Video URL"')[0].split('name="')[-1]
            print('[LÂMTILO]</> Đăng nhập bằng cookie thành công')
            return True
        else:
            print('[LÂMTILO]</> Cookie không hợp lệ hoặc phiên đã hết hạn!')
            return False

    def get_status_services(self):
        request = self.session.get(self.base_url, headers=self.headers).text
        for x in re.findall(r'<h5 class="card-title">.+</h5>\n.+\n.+', request):
            self.services[x.split('<h5 class="card-title">')[1].split('<')[0].strip()] = \
                x.split('d-sm-inline-block">')[1].split('</small>')[0].strip()
        for x in re.findall(r'<h5 class="card-title mb-3">.+</h5>\n<form action=".+">', request):
            self.services_ids[x.split('title mb-3">')[1].split('<')[0].strip()] = \
                x.split('<form action="')[1].split('">')[0].strip()
        for x in re.findall(r'<h5 class="card-title">.+</h5>\n.+<button .+', request):
            self.services_status[x.split('<h5 class="card-title">')[1].split('<')[0].strip()] = \
                False if 'disabled class' in x else True
        return self.services, self.services_status

    def get_table(self):
        table = PrettyTable(field_names=["ID", "DỊCH VỤ", "Trạng Thái"])
        i = 1
        while True:
            if len(self.get_status_services()[0]) > 1:
                break
            else:
                print('[LÂMTILO] Không lấy được dịch vụ, thử lại...')
                time.sleep(2)
        for service in self.services:
            table.add_row([f"{i}", service, self.services[service]])
            i += 1
        print(table)

    def find_video(self):
        if self.service is None:
            return (False, "Chưa chọn dịch vụ")
        while True:
            if self.service not in self.services_ids:
                self.get_status_services()
                time.sleep(1)
            request = self.session.post(
                f'{self.base_url}{self.services_ids[self.service]}',
                headers={
                    'content-type': 'multipart/form-data; boundary=----WebKitFormBoundary0nU8PjANC8BhQgjZ',
                    'user-agent': self.headers['user-agent'],
                    'origin': 'https://zefoy.com'
                },
                data=f'------WebKitFormBoundary0nU8PjANC8BhQgjZ\r\nContent-Disposition: form-data; name="{self.video_key}"\r\n\r\n{self.url}\r\n------WebKitFormBoundary0nU8PjANC8BhQgjZ--\r\n'
            )
            try:
                self.video_info = base64.b64decode(unquote(request.text.encode()[::-1])).decode()
            except:
                time.sleep(3)
                continue

            if 'Session expired' in self.video_info:
                print('[LÂMTILO] Phiên đã hết hạn.')
                return False
            elif 'service is currently not working' in self.video_info:
                return True, '[LÂMTILO] Dịch vụ đang bảo trì.'
            elif """onsubmit="showHideElements""" in self.video_info:
                self.video_info = [
                    self.video_info.split('" name="')[1].split('"')[0],
                    self.video_info.split('value="')[1].split('"')[0]
                ]
                return True, request.text
            elif 'Checking Timer' in self.video_info:
                try:
                    t = int(re.findall(r'ltm=(\d+);', self.video_info)[0])
                except:
                    return False
                while t > 0:
                    print(f"[LÂMTILO] Vui lòng chờ: {t} giây", end="\r")
                    time.sleep(1)
                    t -= 1
                continue
            else:
                print(self.video_info)

    def use_service(self):
        if self.find_video()[0] is False:
            return False
        token = "".join(random.choices(ascii_letters + digits, k=16))
        request = self.session.post(
            f'{self.base_url}{self.services_ids[self.service]}',
            headers={
                'content-type': f'multipart/form-data; boundary=----WebKitFormBoundary{token}',
                'user-agent': self.headers['user-agent'],
                'origin': 'https://zefoy.com'
            },
            data=f'------WebKitFormBoundary{token}\r\nContent-Disposition: form-data; name="{self.video_info[0]}"\r\n\r\n{self.video_info[1]}\r\n------WebKitFormBoundary{token}--\r\n'
        )
        try:
            res = base64.b64decode(unquote(request.text.encode()[::-1])).decode()
        except:
            time.sleep(3)
            return ""

        if 'Session expired' in res:
            print('[LÂMTILO] Phiên đã hết hạn.')
            return ""
        elif 'Too many requests' in res:
            print('[LÂMTILO] Quá nhiều request, chờ tí...')
            time.sleep(3)
        elif 'service is currently not working' in res:
            return '[LÂMTILO] Dịch vụ hiện không hoạt động.'
        else:
            print("[LÂMTILO] ✅ " + res.split("sans-serif;text-align:center;color:green;'>")[1].split("</")[0])


def logo():
    os.system("cls" if os.name == "nt" else "clear")
    print(f"""
{Fore.CYAN}╔════════════════════════════════════════════════════╗
║{Fore.GREEN}       TOOL BUFF VIEW TIKTOK - BY LÂM TILO         {Fore.CYAN}║
╚════════════════════════════════════════════════════╝
{Fore.YELLOW}[!] Đăng nhập bằng PHPSESSID cookie (copy từ trình duyệt Zefoy)
{Fore.YELLOW}[!] Dán link TikTok để gửi view ngay khi đăng nhập thành công
""")


# === MAIN ===
if __name__ == "__main__":
    logo()
    Z = Zefoy()
    if Z.send_cookie_login():
        Z.get_table()
        while True:
            try:
                Z.use_service()
                print(f"{Fore.YELLOW}[LÂMTILO] ➤ Đợi 5 phút rồi gửi tiếp...")
                time.sleep(300)
            except Exception as e:
                print(f"{Fore.RED}[LỖI] {e}")
                time.sleep(10)
    else:
        print(f"{Fore.RED}[LÂMTILO] Cookie không hợp lệ hoặc đã hết hạn.")
