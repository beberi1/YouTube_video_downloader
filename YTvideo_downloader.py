import tkinter as tk
from tkinter import ttk
import yt_dlp


def on_button_click():
    # text = input_field.get("1.0", tk.END).strip()

    selected_options = [audio_var.get(), playlist_var.get()]
    print(audio_var.get())
    
    # print(f"Input Text: {text}")
    # print(f"Checkbox States: {selected_options}")


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
            'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
            'outtmpl': '%(title)s.%(ext)s',
            'merge_output_format': 'mp4',  
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',  
            }],
        }  
    elif (lowQ_var.get() == True):
        ydl_opts = {
            'format': 'bestvideo[height<=240]+bestaudio/best[height<=240]',
            'outtmpl': '%(title)s.%(ext)s',
            'merge_output_format': 'mp4',  
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',  
            }],
        }
    else:
        ydl_opts = {
            'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
            'outtmpl': '%(title)s.%(ext)s',
            'merge_output_format': 'mp4',  
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',  
            }],
        }  
    
    if playlist_var.get():  # მთლიანი ფლეილისთის გადმოწერა
        ydl_opts['noplaylist'] = False
    else:
        ydl_opts['noplaylist'] = True


    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls) 




# menu
root = tk.Tk()
root.title("გადმოიწერე იუთუბიდან")
root.geometry("700x500") 

# input field
input_field = tk.Text(root, height=5, width=80)
input_field.pack(pady=10)

# checkboxes
audio_var = tk.BooleanVar()
playlist_var = tk.BooleanVar()
midQ_var = tk.BooleanVar()
lowQ_var = tk.BooleanVar()

checkbox1 = ttk.Checkbutton(root, text="მარტო აუდიოს გადმოწერა", variable=audio_var)
checkbox2 = ttk.Checkbutton(root, text="მთლიანი ფლეილისთის გადმოწერა", variable=playlist_var)
checkbox3 = ttk.Checkbutton(root, text="720p", variable=midQ_var)
checkbox4 = ttk.Checkbutton(root, text="240p", variable=lowQ_var)



checkbox1.pack(anchor="w", padx=20)
checkbox2.pack(anchor="w", padx=20)
checkbox3.pack(anchor="w", padx=20, pady=20)
checkbox4.pack(anchor="w", padx=20)


# button
button = ttk.Button(root, text="გადმოწერა", command=format_urls)
button.pack(pady=55)

button = ttk.Button(root, text="დირექტორიის გახსნა", command=format_urls)
button.pack(pady=4)




root.mainloop()