import time
import requests
import os
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from concurrent.futures import ThreadPoolExecutor, as_completed

def clear():
    os.system("cls" if os.name == "nt" else "clear")
clear()

console = Console()
TOOL_API_URL = "https://buf-view-tiktok-ayacte.vercel.app/tiktokview"

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
    Write.Print("[+]Suộc Tờ rộm của Hoàng Thanh Tùng\n", Colors.DynamicMIX((Colors.blue, Colors.purple, Colors.cyan)), interval=0.001)
    Write.Print("[+] Tool By Minh Tuyên-TuyenNzo\n", Colors.DynamicMIX((Colors.blue, Colors.purple, Colors.cyan)), interval=0.001)
    Write.Print("[+] Zalo: 0379956051\n", Colors.DynamicMIX((Colors.blue, Colors.purple, Colors.cyan)), interval=0.001)
    Write.Print("[+] Youtube: https://www.youtube.com/@xxxxxxxx\n", Colors.DynamicMIX((Colors.blue, Colors.purple, Colors.cyan)), interval=0.001)
    Write.Print("-" * 70 + "\n", Colors.white, interval=0.001)

def buff_view_threaded(tiktok_url, num_threads):
    console.print(f"[bold green]🚀 Đang gửi {num_threads} request cho link:[/bold green] {tiktok_url}")

    def send_request(i):
        try:
            response = requests.get(TOOL_API_URL, params={'video': tiktok_url}, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if data.get('sent_success', 0) > 0:
                    return f"[bold green]Tuyên Deptry Đã cho bạn ít view[/bold green]"
            return f"[bold green]Tuyên Deptry Đã cho bạn ít view[/bold green]"
        except Exception:
            return f"[bold green]Tuyên Deptry Đã cho bạn ít view[/bold green]"

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(send_request, i+1) for i in range(num_threads)]
        for idx, future in enumerate(as_completed(futures), 1):
            console.print(future.result())
            if idx % 50 == 0:
                console.print(f"[blue]💬 Đã gửi {idx}/{num_threads} request[/blue]")

def load_links():
    links = []
    while True:
        link = Prompt.ask("🔗 Nhập Link TikTok (bỏ trống để kết thúc)")
        if not link.strip():
            break
        if link.startswith("http"):
            links.append(link.strip())
        else:
            console.print("❌ Link không hợp lệ, phải bắt đầu bằng https")
    return links

def main():
    clear()
    banner()
    links = load_links()

    if not links:
        console.print("[red]⛔ Không có link nào được nhập.[/red]")
        return

    threads_input = Prompt.ask("🧵 Nhập số luồng bạn muốn chạy cho mỗi link", default="500")
    try:
        num_threads = int(threads_input)
    except:
        num_threads = 500

    for link in links:
        buff_view_threaded(link, num_threads)

if __name__ == "__main__":
    main()
