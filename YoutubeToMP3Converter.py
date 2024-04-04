from tkinter import *
import customtkinter
from pytube import YouTube
import os
import json
import shutil

# print("Current working directory:", os.getcwd())
class YoutubeToMP3Converter:
    def __init__(self, master):
        self.master = master
        master.title("Youtube to MP3 Converter")
        master.geometry("400x200")
        master.resizable(False, False)

        # Create and place the label
        self.url_label = customtkinter.CTkLabel(master=master, text="URL: ")
        self.url_label.place(relx = 0.1, rely = 0.1)

        # Get the width of the label
        url_label_width = self.url_label.winfo_reqwidth()

        # Define the spacing multiplier factor
        spacing = 0.10

        # Create entry widget for URL input
        self.url_entry = customtkinter.CTkEntry(master=master, placeholder_text="URL")
        self.url_entry.place(relx=0.1 + url_label_width / master.winfo_width() + spacing, rely=0.1)

        # Create button for downloading MP3
        self.download_button = customtkinter.CTkButton(master=master, text="Download MP3", command=self.download_mp3)
        self.download_button.place(relx=0.5, rely=0.6, anchor=CENTER)

        # Create label for displaying download status
        self.display_label = customtkinter.CTkLabel(master=master, text="", wraplength=380)
        self.display_label.place(relx=0.5, rely=0.4, anchor=CENTER)

        # Create label for displaying download progress
        self.percent_progress = customtkinter.CTkLabel(master, text="0%")
        self.percent_progress.place(relx=0.5, rely=0.8, anchor=CENTER)

        # Create progress bar
        self.progressBar = customtkinter.CTkProgressBar(master, width=400)
        self.progressBar.set(0)
        self.progressBar.place(relx=0.5, rely=0.9, anchor=CENTER)


    # Replace special characters in the video title with underscores.
    def sanitize_video_title(self, video_title):
        return video_title.replace("/", "_").replace("[", "_").replace("]", "_")

    def download_mp3(self):
        url = self.url_entry.get()
        with open("config.json") as config_file:
            config = json.load(config_file)
            download_path = config["download_path"]
        try:
            yt = YouTube(url, on_progress_callback=self.on_progress)
            video_title = self.sanitize_video_title(yt.title)
            # Construct the file path with the desired destination directory and video title
            destination = os.path.join(download_path, f"{video_title}.mp3")
            audio_stream = yt.streams.filter(only_audio=True).first()
            audio_stream.download(output_path=os.getcwd(), filename=f"{video_title}.mp3")
            shutil.move(f"{os.getcwd()}/{video_title}.mp3", destination)
            self.display_label.configure(text="MP3 Downloaded", fg_color="green")
            print("MP3 downloaded sucessfully")

        except Exception as e:
            self.display_label.configure(text="Error downloading MP3: " + str(e), fg_color="red")
            print("Error downloading MP3:", e)

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_done = bytes_downloaded / total_size * 100
        percent = str(int(percentage_done))
        self.percent_progress.configure(text=percent + '%')
        self.percent_progress.update()
        
        # update progress bar itself
        self.progressBar.set(float(percentage_done) / 100)

root = customtkinter.CTk()
app = YoutubeToMP3Converter(root)
root.mainloop()