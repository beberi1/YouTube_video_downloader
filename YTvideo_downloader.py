import tkinter as tk
from tkinter import ttk, filedialog
import yt_dlp
import os
import sys
import subprocess
import tempfile


def progress_hook(d):
    """Updates the status label based on download progress."""
    if d['status'] == 'downloading':
        status_label.config(text=f"მიმდინარეობს... {d['_percent_str']}", foreground="#FFD700") 
    elif d['status'] == 'finished':
        status_label.config(text="გადმოწერა დასრულდა!", foreground="#00FF00") 

def open_folder():
    if download_folder:
            if sys.platform.startswith('win'):
                os.startfile(download_folder)
            elif sys.platform.startswith('darwin'):
                subprocess.Popen(['open', download_folder])
            else:  # Linux and others
                subprocess.Popen(['xdg-open', download_folder])

def select_folder():
    global download_folder
    folder = filedialog.askdirectory()
    if folder:
        download_folder = folder
        folder_path_label.config(text=folder, foreground="#9ACBD0")
        save_last_directory(folder) 

def format_urls():
    # Get text input and split by new lines
    urls = input_field.get("1.0", tk.END).strip().split("\n")
    
    # Remove empty lines and spaces
    urls = [url.strip() for url in urls if url.strip()]
    
    if not urls:
        status_label.config(text="გთხოვთ ჩაწეროთ ბმული", foreground="red")
        return

    # Format the URLs into a Python list (უბრალოდ კონსოლში ბეჭდავს თქვენი კოდის მიხედვით)
    formatted_text = "urls = [\n" + "\n".join(f"    '{url}'," for url in urls) + "\n\n    # დაამატე url ები'\n]\n"
    print(formatted_text)

    if (audio_var.get() == True ):
        ydl_opts = {
            'format': 'bestaudio/best',  # Download best audio
            'outtmpl': '%(title)s.%(ext)s',  # Output filename format
            'postprocessors': [{  # Convert to MP3
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',  # You can change to '320' for better quality
            }],
        }
    elif (midQ_var.get() == True):
        ydl_opts = {
            'format': 'bestvideo[height<=720][ext=mp4]+bestaudio/best[ext=mp4]',
            'outtmpl': '%(title)s.%(ext)s',
            'merge_output_format': 'mp4',  
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',  
            }],
        }
    elif (lowQ_var.get() == True):
        ydl_opts = {
            'format': 'bestvideo[height<=240][ext=mp4]+bestaudio/best[ext=mp4]',
            'outtmpl': '%(title)s.%(ext)s',
            'merge_output_format': 'mp4',  
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',  
            }],
        }
    else:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio/best[ext=mp4]',
                'outtmpl': f"{download_folder}/%(title)s.%(ext)s",
                'merge_output_format': 'mp4',
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
        }  
        
    status_label.config(text="გადმოწერა დაიწყო...", foreground="#9ACBD0")
    root.update_idletasks()  # Update GUI immediately

    if playlist_var.get():  # მთლიანი ფლეილისთის გადმოწერა
        ydl_opts['noplaylist'] = False
    else:
        ydl_opts['noplaylist'] = True

    if download_folder:
        ydl_opts['outtmpl'] = f"{download_folder}/%(title)s.%(ext)s"
    else:
        status_label.config(text="აირჩიეთ ფოლდერი!", foreground="red")
        return
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(urls)
            status_label.config(text="გადმოწერა დასრულდა!", foreground="#00FF00")
    except Exception as e:
        status_label.config(text=f"შეცდომა: {str(e)}", foreground="red")

# ფაილის სისტემის ლოგიკა
CONFIG_FILE = os.path.join(tempfile.gettempdir(), "yt_gui_lastdir.txt")

def load_last_directory():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""

def save_last_directory(folder):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write(folder)

download_folder = load_last_directory()

# --- GUI ნაწილი ---

root = tk.Tk()
root.title("გადმოწერე იუთუბიდან")
root.geometry("750x533")

# --- აიქონის დაყენება ---
# ეს კოდი პოულობს სკრიპტის მიმდინარე საქაღალდეს და ეძებს icon.ico-ს
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(script_dir, "icon.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)
except Exception as e:
    print(f"აიქონი ვერ დაყენდა: {e}") # თუ რამე შეცდომაა, უბრალოდ კონსოლში დაწერს
# ------------------------


# ფერების პალიტრა (Modern Dark Theme)
bg_color = "#2b2b2b"
fg_color = "#ffffff"
accent_color = "#9ACBD0"
input_bg = "#383838"

root.configure(bg=bg_color)

# სტილის კონფიგურაცია
style = ttk.Style()
style.theme_use('clam') # უფრო სუფთა თემა

# ზოგადი სტილები
style.configure("TFrame", background=bg_color)
style.configure("TLabel", background=bg_color, foreground=fg_color, font=("Segoe UI", 10))
style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground=accent_color)
style.configure("Status.TLabel", font=("Segoe UI", 10, "italic"))

# ღილაკების სტილი
style.configure("TButton", 
                font=("Segoe UI", 10, "bold"), 
                background=accent_color, 
                foreground="#000000", 
                borderwidth=0, 
                focuscolor="none")
style.map("TButton", background=[("active", "#7aaeb3")]) # დაჭერის ეფექტი

# ჩექბოქსების სტილი
style.configure("TCheckbutton", background=bg_color, foreground=fg_color, font=("Segoe UI", 10))
style.map("TCheckbutton", background=[("active", bg_color)])

# ლეიბლ ფრეიმის სტილი (ჩარჩოები)
style.configure("TLabelframe", background=bg_color, foreground=accent_color, bordercolor="#555555")
style.configure("TLabelframe.Label", background=bg_color, foreground=accent_color, font=("Segoe UI", 10, "bold"))


# --- მთავარი კონტეინერი ---
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill="both", expand=True)

# სათაური
title_label = ttk.Label(main_frame, text="ვიდეოს & აუდიოს იუთუბიდან გადმომწერი", style="Header.TLabel")
title_label.pack(pady=(0, 15))


# 1. ბმულების სექცია
input_frame = ttk.LabelFrame(main_frame, text=" ბმულები (თითო ხაზზე თითო) ", padding="10")
input_frame.pack(fill="x", pady=5)

# სქროლიანი ტექსტის ველი
input_scroll = ttk.Scrollbar(input_frame)
input_scroll.pack(side="right", fill="y")

input_field = tk.Text(input_frame, height=5, font=("Consolas", 10), 
                      bg=input_bg, fg="white", insertbackground="white", 
                      borderwidth=0, yscrollcommand=input_scroll.set)
input_field.pack(fill="x", side="left", expand=True)
input_scroll.config(command=input_field.yview)

# 2. პარამეტრების სექცია
options_frame = ttk.LabelFrame(main_frame, text=" პარამეტრები ", padding="10")
options_frame.pack(fill="x", pady=10)

audio_var = tk.BooleanVar()
playlist_var = tk.BooleanVar()
midQ_var = tk.BooleanVar()
lowQ_var = tk.BooleanVar()

# ჩექბოქსების ბადე (Grid)
c1 = ttk.Checkbutton(options_frame, text="მხოლოდ აუდიო (MP3)", variable=audio_var)
c2 = ttk.Checkbutton(options_frame, text="მთლიანი ფლეილისთი", variable=playlist_var)
c3 = ttk.Checkbutton(options_frame, text="ხარისხი: 720p", variable=midQ_var)
c4 = ttk.Checkbutton(options_frame, text="ხარისხი: 240p (დაბალი)", variable=lowQ_var)

c1.grid(row=0, column=0, sticky="w", padx=20, pady=5)
c2.grid(row=0, column=1, sticky="w", padx=20, pady=5)
c3.grid(row=1, column=0, sticky="w", padx=20, pady=5)
c4.grid(row=1, column=1, sticky="w", padx=20, pady=5)

# 3. შენახვის ადგილის სექცია
folder_frame = ttk.LabelFrame(main_frame, text=" შენახვის ადგილი ", padding="10")
folder_frame.pack(fill="x", pady=5)

# ბილიკის ჩვენება
folder_display_text = download_folder if download_folder else "არ არის არჩეული"
folder_color = accent_color if download_folder else "#888888"

folder_path_label = ttk.Label(folder_frame, text=folder_display_text, foreground=folder_color, font=("Segoe UI", 9))
folder_path_label.pack(side="left", fill="x", expand=True, padx=(0, 10))

btn_select = ttk.Button(folder_frame, text="შეცვლა", command=select_folder, width=10)
btn_select.pack(side="right", padx=5)

btn_open = ttk.Button(folder_frame, text="გახსნა", command=open_folder, width=10)
btn_open.pack(side="right")

# 4. მოქმედების სექცია (ღილაკი და სტატუსი)
action_frame = ttk.Frame(main_frame, padding="20 10 20 0")
action_frame.pack(fill="x", pady=10)

download_button = ttk.Button(action_frame, text="გადმოწერა", command=format_urls, style="TButton")
download_button.pack(fill="x", ipady=5) # ipady ზრდის ღილაკის სიმაღლეს

status_label = ttk.Label(action_frame, text="მზადაა სამუშაოდ", style="Status.TLabel", anchor="center")
status_label.pack(pady=(10, 0))

# ფანჯრის ცენტრირება
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

root.mainloop()