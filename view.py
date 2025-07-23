import time
import requests
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


''',
                Colors.DynamicMIX((Colors.blue, Colors.purple, Colors.cyan)),
                interval=0.001)

    Write.Print("-" * 70 + "\n", Colors.white, interval=0.001)
    Write.Print("[+] Tool By Minh Tuyên-TuyenNzo\n",
                Colors.DynamicMIX((Colors.blue, Colors.purple, Colors.cyan)),
                interval=0.001)
    Write.Print("[+] Zalo: 0379956051\n",
                Colors.DynamicMIX((Colors.blue, Colors.purple, Colors.cyan)),
                interval=0.001)
    Write.Print("[+] Youtube: https://www.youtube.com/@xxxxxxxx\n",
                Colors.DynamicMIX((Colors.blue, Colors.purple, Colors.cyan)),
                interval=0.001)
    Write.Print("-" * 70 + "\n", Colors.white, interval=0.001)

def buff_view(tiktok_url, loop_num=None):
    try:
        response = requests.get(TOOL_API_URL, params={'video': tiktok_url}, timeout=60)

        if response.status_code != 200:
            console.print(f"❌ [red]Loi HTTP {response.status_code} tu API[/red]")
            return

        data = response.json()
        result_panel = Panel.fit(
            f"""🔁 Lan: {loop_num if loop_num else 1}
🔗 Link: [bold cyan]{tiktok_url}[/bold cyan]
📹 Video ID: [bold magenta]{data.get('video_id', 'N/A')}[/bold magenta]
✅ Thanh cong: [green]{data.get('sent_success', 0)}[/green]
❌ That bai: [red]{data.get('sent_fail', 0)}[/red]
🕒 Xu ly: [italic yellow]{round(data.get('time_used', 0), 2)} giay[/italic yellow]
🧰 Proxy: [italic]{data.get('proxy_used', 'Khong ro')}[/italic]
⏱️ View se tang dan sau vai phut...
""",
            title=f"🎉 KET QUA [{loop_num if loop_num else 1}]", border_style="bright_magenta"
        )
        console.print(result_panel)

    except requests.exceptions.Timeout:
        console.print("[bold yellow]⏳ Tool xu ly lau hon du kien. View co the van đang tang.[/bold yellow]")
    except Exception as e:
        console.print(f"[bold red]⚠️ Loi khi goi API: {e}[/bold red]")

def buff_view_1000_times(tiktok_url):
    console.print(f"[bold green]🚀 Dang tien hanh 1000 request mot lan cho link:[/bold green] {tiktok_url}")

    def send_single_request(i):
        try:
            response = requests.get(TOOL_API_URL, params={'video': tiktok_url}, timeout=30)
            if response.status_code == 200:
                data = response.json()
                return f"✅ [Thread {i}] Thanh cong: {data.get('sent_success', 0)} | That bai: {data.get('sent_fail', 0)}"
            else:
                return f"❌ [Thread {i}] Loi HTTP {response.status_code}"
        except Exception as e:
            return f"⚠️ [Thread {i}] Loi: {e}"

    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(send_single_request, i+1) for i in range(1000)]
        for idx, future in enumerate(as_completed(futures), 1):
            console.print(future.result())
            if idx % 100 == 0:
                console.print(f"[blue]💬 Da gui {idx}/1000 request[/blue]")

def auto_loop_multi(links: list, delay_sec: int, max_workers=5):
    console.print(Panel(f"[bold yellow]🔁 TREO TOOL ĐANG CHAY VOI {len(links)} LINK (Đa luong)[/bold yellow]\n"
                        f"⏱️ Delay giua moi vong: {delay_sec} giay\n"
                        f"🧵 So luong toi đa: {max_workers}\n"
                        f"❌ Nhan [red]Ctrl + C[/red] đe dung", title="⚙️ AUTO MULTI-THREAD MODE", border_style="bright_green"))

    loop = 1
    try:
        while True:
            console.print(f"\n[bold blue]🔄 Vong lap #{loop}[/bold blue]")

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {executor.submit(buff_view, link, loop): link for link in links}
                for future in as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        console.print(f"[red]⚠️ Loi trong luong: {e}[/red]")

            loop += 1
            time.sleep(delay_sec)
    except KeyboardInterrupt:
        console.print("\n[bold red]🛑 Da dung treo tool theo yeu cau.[/bold red]")

def load_links_input():
    links = []
    while True:
        link = Prompt.ask("🔗 Nhap link TikTok (hoac de trong de ket thuc)")
        if not link.strip():
            break
        if link.startswith("http"):
            links.append(link.strip())
        else:
            console.print("❌ [red]Link khong hop le, phai bat dau bang http[/red]")
    return links

def load_links_from_file(file_path):
    links = []
    try:
        with open(file_path, "r") as f:
            for line in f:
                clean_link = line.strip()
                if clean_link.startswith("http"):
                    links.append(clean_link)
    except Exception as e:
        console.print(f"[red]⚠️ Khong the doc file: {e}[/red]")
    return links

def main():
    banner()

    if Confirm.ask("📁 Tai danh sach link tu file .txt?", default=False):
        file_path = Prompt.ask("📄 Nhap duong dan file (moi dong 1 link)", default="links.txt")
        links = load_links_from_file(file_path)
    else:
        links = load_links_input()

    if not links:
        console.print("[red]❌ Khong co link hop le nao de treo.[/red]")
        return

    if Confirm.ask("🚀 Ban co muon gui 1000 request mot lan cho tung link?", default=True):
        for link in links:
            buff_view_1000_times(link)
        return

    delay = Prompt.ask("⏱️ Nhap thoi gian delay giua moi vong lap (giay)", default="60")
    try:
        delay_sec = int(delay)
    except:
        console.print("[red]❌ Delay khong hop le. Dung mac dinh 60s.[/red]")
        delay_sec = 60

    workers = Prompt.ask("🧵 Nhap so luong luong xu ly dong thoi", default="5")
    try:
        max_workers = int(workers)
    except:
        console.print("[red]❌ So luong khong hop le. Dung mac dinh 5.[/red]")
        max_workers = 5

    auto_loop_multi(links, delay_sec, max_workers)

if __name__ == "__main__":
    main()
