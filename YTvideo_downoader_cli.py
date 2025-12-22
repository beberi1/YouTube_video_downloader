import yt_dlp
import os
import sys

# ფერები ტერმინალის სილამაზისთვის
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("╔═══════════════════════════════════════════════╗")
    print("║          YOUTUBE DOWNLOADER CLI v1.0          ║")
    print("║       იუთუბის ვიდეოს გადმოწერი CLI v1.0     ║")
    print("╚═══════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}")

def get_urls():
    print(f"{Colors.CYAN}[?] ჩაწერე ვიდეოს ბმულები (დააჭირე Enter-ს თითო ბმულის შემდეგ).")
    print(f"    როცა მორჩები, დააჭირე Enter-ს ცარიელ ხაზზე:{Colors.ENDC}")
    urls = []
    while True:
        url = input(f"{Colors.BLUE}>> {Colors.ENDC}").strip()
        if not url:
            break
        urls.append(url)
    return urls

def get_options():
    print(f"\n{Colors.CYAN}[?] აირჩიე გადმოწერის ტიპი:{Colors.ENDC}")
    print(" 1. მარტო აუდიო (MP3)")
    print(" 2. ვიდეო - საუკეთესო ხარისხი")
    print(" 3. ვიდეო - 720p")
    print(" 4. ვიდეო - 240p")
    
    choice = input(f"{Colors.WARNING}>> აირჩიე ნომერი [1-4]: {Colors.ENDC}").strip()
    
    is_audio = False
    quality = "best"
    
    if choice == '1':
        is_audio = True
    elif choice == '3':
        quality = "720"
    elif choice == '4':
        quality = "240"
    # choice 2 is default (best)

    print(f"\n{Colors.CYAN}[?] ფლეილისთია?{Colors.ENDC}")
    pl_input = input(f"{Colors.WARNING}>> გადმოვწერო მთლიანი სია? (y/N): {Colors.ENDC}").lower()
    playlist = True if pl_input == 'y' else False

    return is_audio, quality, playlist

def get_directory():
    print(f"\n{Colors.CYAN}[?] სად შევინახო?{Colors.ENDC}")
    current_dir = os.getcwd()
    print(f"    (დატოვე ცარიელი, რომ შეინახოს აქ: {Colors.BOLD}{current_dir}{Colors.ENDC})")
    path = input(f"{Colors.BLUE}>> {Colors.ENDC}").strip()
    
    if not path:
        return current_dir
    
    if not os.path.exists(path):
        try:
            create = input(f"{Colors.FAIL}დირექტორია არ არსებობს. შევქმნა? (y/N): {Colors.ENDC}").lower()
            if create == 'y':
                os.makedirs(path)
                return path
            else:
                print("გადმოწერა გაუქმდა.")
                sys.exit()
        except Exception as e:
            print(f"შეცდომა: {e}")
            sys.exit()
    return path

def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '').strip()
        # ვშლით წინა ხაზს რომ ლამაზად განახლდეს
        sys.stdout.write(f"\r{Colors.GREEN}   ⏳ მიმდინარეობს: {percent} {Colors.ENDC}")
        sys.stdout.flush()
    elif d['status'] == 'finished':
        print(f"\n{Colors.BOLD}{Colors.GREEN}   [V] გადმოწერა დასრულდა! მუშავდება...{Colors.ENDC}")

def main():
    print_banner()
    
    # 1. URL-ების მიღება
    urls = get_urls()
    if not urls:
        print(f"{Colors.FAIL}ბმულები არ არის მითითებული!{Colors.ENDC}")
        return

    # 2. პარამეტრების არჩევა
    is_audio, quality, playlist = get_options()
    
    # 3. საქაღალდის არჩევა
    save_path = get_directory()


    opts = {
        'outtmpl': f"{save_path}/%(title)s.%(ext)s",
        'noplaylist': not playlist,
        'progress_hooks': [progress_hook],
        'quiet': True,        # ზედმეტი ტექსტი რომ არ იყოს
        'no_warnings': True,
    }

    if is_audio:
        opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
        })
    elif quality == "720":
        opts.update({
            'format': 'bestvideo[height<=720][ext=mp4]+bestaudio/best[ext=mp4]',
            'merge_output_format': 'mp4',
            'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}],
        })
    elif quality == "240":
        opts.update({
            'format': 'bestvideo[height<=240][ext=mp4]+bestaudio/best[ext=mp4]',
            'merge_output_format': 'mp4',
            'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}],
        })
    else: # Best
        opts.update({
            'format': 'bestvideo[ext=mp4]+bestaudio/best[ext=mp4]',
            'merge_output_format': 'mp4',
            'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}],
        })

    # 5. გადმოწერის დაწყება
    print(f"\n{Colors.HEADER}--- იწყება {len(urls)} ფაილის გადმოწერა ---{Colors.ENDC}")
    
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download(urls)
        print(f"\n{Colors.BOLD}{Colors.GREEN}🎉 ყველა ოპერაცია წარმატებით დასრულდა!{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.FAIL}❌ დაფიქსირდა შეცდომა: {str(e)}{Colors.ENDC}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.FAIL}შეწყდა მომხმარებლის მიერ.{Colors.ENDC}")