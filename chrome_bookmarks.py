from tkinter import *
import customtkinter
from pytube import YouTube
import os


# script_directory = os.getcwd()

# if os.access(script_directory, os.W_OK):
#     print("Has write perm: ", script_directory)
# else:
#     print("DOES NOT have write perm: ", script_directory)

def download_mp3():
    url = url_entry.get()
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_stream.download(filename='audio.mp3')
        display_label.configure(text="MP3 Downloaded", fg_color="green")
        print("MP3 downloaded sucessfully")

    except Exception as e:
        display_label.configure(text="Error downloading MP3: " + str(e), fg_color="red")
        print("Error downloading MP3:", e)


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_done = bytes_downloaded / total_size * 100
    percent = str(int(percentage_done))
    percent_progress.configure(text=percent + '%')
    percent_progress.update()
    # print(percentage_done)
    
    # update progress bar itself
    progressBar.set(float(percentage_done) / 100)


root = customtkinter.CTk()
root.title("Youtube to MP3 Converter")
root.geometry("400x200")
root.resizable(False, False)

# Create and place the label
url_label = customtkinter.CTkLabel(master=root, text="URL: ")
url_label.place(relx = 0.1, rely = 0.1)

# Get the width of the label
url_label_width = url_label.winfo_reqwidth()

# Define the spacing multiplier factor
spacing = 0.10

# Create entry widget for URL input
url_entry = customtkinter.CTkEntry(master=root, placeholder_text="URL")
url_entry.place(relx=0.1 + url_label_width / root.winfo_width() + spacing, rely=0.1)

# Create button for downloading MP3
download_button = customtkinter.CTkButton(master=root, text="Download MP3", command=download_mp3)
download_button.place(relx=0.5, rely=0.6, anchor=CENTER)

# Create label for displaying download status
display_label = customtkinter.CTkLabel(master=root, text="", wraplength=380)
display_label.place(relx=0.5, rely=0.4, anchor=CENTER)

percent_progress = customtkinter.CTkLabel(root, text="0%")
percent_progress.place(relx=0.5, rely=0.8, anchor=CENTER)

progressBar = customtkinter.CTkProgressBar(root, width=400)
progressBar.set(0)
progressBar.place(relx=0.5, rely=0.9, anchor=CENTER)

root.mainloop()