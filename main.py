import os
import requests
import time

# --- CẤU HÌNH MÀU SẮC (ANSI COLORS) ---
class Col:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

# --- HÀM LẤY IP ---
def get_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        return response.json().get("ip")
    except:
        return "Dang kiem tra..."

# --- HÀM BANNER (BẠN TỰ SỬA NẾU CẦN) ---
def banner():
    # Xóa màn hình
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # 1. Dòng bản quyền
    print(f"{Col.RED} © Bản Quyền AnhTuyenDz{Col.RESET}")
    print("")

    # 2. ASCII Art (Tôi đã chèn mẫu bạn gửi vào đây)
    print(f"{Col.CYAN}        ████████╗███╗   ██╗███████╗ ██████╗ {Col.RESET}")
    print(f"{Col.CYAN}        ╚══██╔══╝████╗  ██║╚══███╔╝██╔═══██╗{Col.RESET}")
    print(f"{Col.CYAN}           ██║   ██╔██╗ ██║  ███╔╝ ██║   ██║{Col.RESET}")
    print(f"{Col.CYAN}           ██║   ██║╚██╗██║ ███╔╝  ██║   ██║{Col.RESET}")
    print(f"{Col.CYAN}           ██║   ██║ ╚████║███████╗╚██████╔╝{Col.RESET}")
    print(f"{Col.CYAN}           ╚═╝   ╚═╝  ╚═══╝╚══════╝ ╚═════╝ {Col.RESET}")
    
    # 3. Đường kẻ phân cách
    print(f"{Col.CYAN}------------------------------------------------------------{Col.RESET}")

# --- HÀM MAIN CHÍNH ---
def main():
    # Lấy IP trước khi hiện menu
    current_ip = get_ip()

    # Hiện Banner
    banner()

    # --- PHẦN THÔNG TIN LIÊN HỆ ---
    # Cấu trúc: [</>] => Tiêu đề: Nội dung
    print(f"{Col.RED}[</>]{Col.RESET} => {Col.YELLOW}Admin:{Col.RESET}       {Col.GREEN}Minh Tuyên{Col.RESET}")
    print(f"{Col.RED}[</>]{Col.RESET} => {Col.YELLOW}Techcombank:{Col.RESET} {Col.WHITE}4321032007{Col.RESET}")
    print(f"{Col.RED}[</>]{Col.RESET} => {Col.YELLOW}Facebook:{Col.RESET}    {Col.WHITE}https://www.facebook.com/dhphuoc.207{Col.RESET}")
    print(f"{Col.RED}[</>]{Col.RESET} => {Col.YELLOW}Zalo:{Col.RESET}        {Col.WHITE}https://zalo.me/g/ucvski448{Col.RESET}")
    
    print(f"{Col.CYAN}------------------------------------------------------------{Col.RESET}")

    # --- PHẦN THÔNG TIN MÁY CHỦ (BOX) ---
    print(f"{Col.CYAN}╔═══════════════════════════════╗{Col.RESET}")
    print(f"{Col.CYAN}║       Thông Tin Máy Chủ       ║{Col.RESET}")
    print(f"{Col.CYAN}╚═══════════════════════════════╝{Col.RESET}")
    
    print(f"{Col.RED}[</>]{Col.RESET} => {Col.YELLOW}Phiên Bản:{Col.RESET}  {Col.GREEN}1.0.1{Col.RESET}")
    print(f"{Col.RED}[</>]{Col.RESET} => {Col.YELLOW}IP Của Bạn:{Col.RESET} {Col.GREEN}{current_ip}{Col.RESET}")
    
    print(f"{Col.CYAN}------------------------------------------------------------{Col.RESET}")

    # --- PHẦN MENU TOOL (BOX) ---
    print(f"{Col.CYAN}╔═══════════════════════════════╗{Col.RESET}")
    print(f"{Col.CYAN}║       Tool facebook           ║{Col.RESET}")
    print(f"{Col.CYAN}╚═══════════════════════════════╝{Col.RESET}")
    
    print(f"{Col.RED}[</>]{Col.RESET} => {Col.YELLOW}Nhập [1.1] Để Chọn Chế Độ Facebook{Col.RESET}")
    print("")

    # --- NHẬP LỰA CHỌN ---
    while True:
        try:
            choice = input(f"{Col.RED}[</>]{Col.RESET} => {Col.YELLOW}Nhập Lựa Chọn: {Col.RESET}")
            
            if choice == "1.1":
                print(f"\n{Col.GREEN}>> Đang khởi động Tool Facebook...{Col.RESET}")
                time.sleep(1)
                # GỌI HÀM TOOL FACEBOOK CỦA BẠN Ở ĐÂY
                # facebook_tool()
                break
            else:
                print(f"{Col.RED}>> Lựa chọn không hợp lệ!{Col.RESET}")
        except KeyboardInterrupt:
            print("\nĐã thoát tool.")
            break

if __name__ == "__main__":
    main()
