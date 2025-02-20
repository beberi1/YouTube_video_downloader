import tkinter as tk
from tkinter import ttk, filedialog
import yt_dlp
import os
import sys
import subprocess

# Global variable for download folder
download_folder = ""

def progress_hook(d):
    """Updates the status label based on download progress."""
    if d['status'] == 'downloading':
        status_label.config(text=f"გადმოწერა მიმდინარეობს... {d['_percent_str']}", foreground="blue")
    elif d['status'] == 'finished':
        status_label.config(text="გადმოწერა დასრულდა!", foreground="green")

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
        folder_label.config(text=f"აირჩეული დირექტორია: {folder}", foreground="green")


# გადმოწერის ლოგიკები
def format_urls():
        # Get text input and split by new lines
    urls = input_field.get("1.0", tk.END).strip().split("\n")
    
    # Remove empty lines and spaces
    urls = [url.strip() for url in urls if url.strip()]
    
    # Format the URLs into a Python list
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
            'format': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/mp4',
            'outtmpl': '%(title)s.%(ext)s',
            'merge_output_format': 'mp4',  
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',  
            }],
        }
    elif (lowQ_var.get() == True):
        ydl_opts = {
            'format': 'bestvideo[height<=240][ext=mp4]+bestaudio[ext=m4a]/mp4',
            'outtmpl': '%(title)s.%(ext)s',
            'merge_output_format': 'mp4',  
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',  
            }],
        }
    else:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
                'outtmpl': f"{download_folder}/%(title)s.%(ext)s",
                'merge_output_format': 'mp4',
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
        }  
        
    status_label.config(text="გადმოწერა დაიწყო...", foreground="blue")
    root.update_idletasks()  # Update GUI immediately

    
    if playlist_var.get():  # მთლიანი ფლეილისთის გადმოწერა
        ydl_opts['noplaylist'] = False
    else:
        ydl_opts['noplaylist'] = True

    if download_folder:
        ydl_opts['outtmpl'] = f"{download_folder}/%(title)s.%(ext)s"
    else:
        return
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)
        status_label.config(text="გადმოწერა დასრულდა!", foreground="green")



# Create main window
root = tk.Tk()
root.title("გადმოიწერე იუთუბიდან")
root.geometry("700x400")
root.configure(bg="#9ACBD0")  # Dark background color

# Define styles
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 14), padding=10, background="#9ACBD0", foreground="black")
style.configure("TCheckbutton", font=("Helvetica", 12), padding=5, background="#9ACBD0", foreground="white")
style.configure("TLabel", font=("Helvetica", 12), background="#9ACBD0", foreground="white")

# Input frame
input_frame = ttk.Frame(root, padding="10 10 10 10", style="TFrame")
input_frame.pack(fill="x")

input_label = ttk.Label(input_frame, text="ჩაწერე ბმულები | Enter-ით გამოტოვე", style="TLabel")
input_label.pack(anchor="w")
input_field = tk.Text(input_frame, height=5, width=80, font=("Helvetica", 12), bg="#9ACBD0", fg="white")
input_field.pack(pady=5)

# Checkbox frame
checkbox_frame = ttk.Frame(root, padding="10 10 10 10")
checkbox_frame.pack(fill="x")

audio_var = tk.BooleanVar()
playlist_var = tk.BooleanVar()
midQ_var = tk.BooleanVar()
lowQ_var = tk.BooleanVar()

checkbox1 = ttk.Checkbutton(checkbox_frame, text="მარტო აუდიოს გადმოწერა", variable=audio_var)
checkbox2 = ttk.Checkbutton(checkbox_frame, text="მთლიანი ფლეილისთის გადმოწერა", variable=playlist_var)
checkbox3 = ttk.Checkbutton(checkbox_frame, text="720p", variable=midQ_var)
checkbox4 = ttk.Checkbutton(checkbox_frame, text="240p", variable=lowQ_var)
status_label = ttk.Label(root, text="", font=("Helvetica", 12), foreground="black")


status_label.pack(pady=5)
checkbox1.grid(row=0, column=0, sticky="w", padx=10, pady=5)
checkbox2.grid(row=0, column=1, sticky="w", padx=10, pady=5)
checkbox3.grid(row=1, column=0, sticky="w", padx=10, pady=5)
checkbox4.grid(row=1, column=1, sticky="w", padx=10, pady=5)

# Action frame
action_frame = ttk.Frame(root, padding="10 10 10 10")
action_frame.pack(fill="x")

download_button = ttk.Button(action_frame, text="გადმოწერა", command=format_urls, style="TButton")
download_button.grid(row=0, column=0, padx=10, pady=10)

folder_button = ttk.Button(action_frame, text="არჩევა", command=select_folder, style="TButton")
folder_button.grid(row=0, column=1, padx=10, pady=10)

folder_label = ttk.Label(action_frame, text="დირექტორია არ არის არჩეული", foreground="red", background="#F2EFE7")
folder_label.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

open_folder_button = ttk.Button(action_frame, text="გახსნა", command=open_folder)
open_folder_button.grid(row=0, column=3, padx=10, pady=10)

root.mainloop()
