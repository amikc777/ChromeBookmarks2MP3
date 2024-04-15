from tkinter import *
import customtkinter
from pytube import YouTube
import os
import threading
from queue import Queue
import json
import shutil


class YoutubeToMP3Converter:
    """
    Initialize the YoutubeToMP3Converter class with GUI elements
    and setup necessary attributes for downloading MP3s.

    Parameters:
    - master: tkinter master widget
    - integrated: flag to indicate integration with another script
    """
    def __init__(self, master, integrated=False):
        self.master = master
        master.title("Youtube to MP3 Converter")
        master.geometry("400x200")
        master.resizable(False, False)

        # Create and place the label
        self.url_label = customtkinter.CTkLabel(master=master, text="URL: ")
        self.url_label.place(relx=0.1, rely=0.1)

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

        self.url_queue = Queue()
        self.processing = False  # Flag to indicate if a download is in progress
        self.integrated = integrated  # Flag to indicate if integrated into the second script
        self.total_urls = 0  # Total number of URLs to process
        self.downloaded_count = 0  # Counter for successfully downloaded songs


    def sanitize_video_title(self, video_title):
        """
        Sanitize the video title to replace characters that may cause issues
        when saving the MP3 file.
        """
        return video_title.replace("/", "_").replace("[", "_").replace("]", "_").replace("|", "_").replace('"', "_")


    def enqueue_url(self, url):
        """
        Add a URL to the processing queue and increment the total count of URLs.
        Start processing if no download is in progress.
        """
        self.url_queue.put(url)
        self.total_urls += 1  # Increment total number of URLs

        if not self.processing:
            self.process_next_url()


    def download_mp3(self):
        """
        Triggered by the "Download MP3" button.
        Retrieves URL from the entry widget and starts the download process.
        Updates display to show "Looking up song..." while processing.
        """
        url = self.url_entry.get()
        self.display_label.configure(text="Looking up song...", fg_color="blue")

        # Add URL to the queue for processing
        self.enqueue_url(url)


    def download_thread(self, url):
        """
        Worker thread function to download MP3 from the provided URL.
        Handles downloading, progress updates, and error handling.
        Updates display label and console output upon completion.
        """
        try:
            with open("config.json") as config_file:
                config = json.load(config_file)
                download_path = config["download_path"]

            yt = YouTube(url, on_progress_callback=self.on_progress)
            video_title = self.sanitize_video_title(yt.title)
            destination = os.path.join(download_path, f"{video_title}.mp3")
            audio_stream = yt.streams.filter(only_audio=True).first()
            audio_stream.download(output_path=os.getcwd(), filename=f"{video_title}.mp3")
            shutil.move(f"{os.getcwd()}/{video_title}.mp3", destination)

            # Update display label and console output
            self.display_label.configure(text="MP3 Downloaded", fg_color="green")
            print("MP3 downloaded successfully")

        except Exception as e:
            self.display_label.configure(text="Error downloading MP3: " + str(e), fg_color="red")
            print("Error downloading MP3:", e)

        self.processing = False
        if self.integrated:  # Check if integrated mode
            self.downloaded_count += 1  # Increment downloaded count

            if self.downloaded_count == self.total_urls:
                # Schedule the script to exit after 10 seconds
                self.master.after(10000, self.exit_script)
            else:
                self.process_next_url()


    def process_next_url(self):
        """
        Process the next URL in the queue if available.
        Starts a new thread to download the URL.
        """
        if not self.url_queue.empty():
            url = self.url_queue.get()
            self.processing = True
            threading.Thread(target=self.download_thread, args=(url,)).start()


    def exit_script(self):
        """
        Exit the script by quitting the tkinter application.
        """
        if self.master:
            self.master.quit()


    def on_progress(self, stream, chunk, bytes_remaining):
        """
        Callback function to update download progress.

        Parameters:
        - stream: the pytube stream object
        - chunk: chunk size of the download
        - bytes_remaining: remaining bytes to download
        """
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_done = bytes_downloaded / total_size * 100
        percent = str(int(percentage_done))
        self.percent_progress.configure(text=percent + '%')
        self.percent_progress.update()
        
        # Update progress bar
        self.progressBar.set(float(percentage_done) / 100)


def main():
    """
    Entry point of the program.
    Creates a Tkinter root window and initializes the YoutubeToMP3Converter application.
    Starts the main event loop to handle GUI interactions.
    """
    root = customtkinter.CTk()
    app = YoutubeToMP3Converter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
