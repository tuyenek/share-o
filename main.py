import requests
import os
from pystyle import Write, Colors
import time
trang = "\033[1;37m"
xanh_la = "\033[1;32m"
xanh_duong = "\033[1;34m"
do = "\033[1;31m"
vang = "\033[1;33m"
tim = "\033[1;35m"
dac_biet = "\033[32;5;245m\033[1m\033[38;5;39m"
kt_code = "</>"
reset = "\033[0m"
def clear():
    os.system("cls" if os.name == "nt" else "clear")
print('Loading...')
time.sleep(3)

clear()


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


banner()
Write.Print("-" * 70 + "\n", Colors.white, interval=0.001)
Write.Print(r'''
╔═══════════════════════════════╗              
║       Tool By Tuyên           ║                                                       
╚═══════════════════════════════╝
''',
            Colors.cyan,
            interval=0.001)
print(
    f'{do}[{trang}</>{do}] {trang} => {xanh_la} Nhập {do}[{vang}1{do}]{xanh_la} Để chọn chế độ Buff Shara Ảo Facebook'
)
print(
    f'{do}[{trang}</>{do}] {trang} => {xanh_la} Nhập {do}[{vang}2{do}]{xanh_la} Để chọn chế độ Buff View tiktok đa luồng'
)
while True:
    print(f'{do}[{trang}{kt_code}{do}] {trang} => {xanh_la} Chọn Chế độ: {reset}',
          end="")
    chedo = input()
    if chedo == "1":
        exec(
            requests.get(
                'https://raw.githubusercontent.com/tuyenek/share-o/main/share.py'
            ).text)
    elif chedo == "2":
        exec(
            requests.get(
                'https://raw.githubusercontent.com/tuyenek/share-o/refs/heads/main/buffv.py?nocache=1'
            ).text)
    else:
        print(f'{do} chọn sai rồi kìa? tay bị tật à thằng ngu')
