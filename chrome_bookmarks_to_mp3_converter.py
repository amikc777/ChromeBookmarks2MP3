import customtkinter
from chrome_bookmarks_parser import ChromeBookmarksParser
from youtube_to_mp3_converter import YoutubeToMP3Converter

def process_folder_urls(folder_name):
    chrome_bookmarks_config_path = 'config.json'
    parser = ChromeBookmarksParser(chrome_bookmarks_config_path)
    folder_urls = parser.find_folder_urls(folder_name)
    return folder_urls

def main():
    folder_name = input("Enter the name of the folder to process: ")
    folder_urls = process_folder_urls(folder_name)

    if folder_urls:
        print("Found URLs in folder:", folder_urls)
        root = customtkinter.CTk()
        app = YoutubeToMP3Converter(root, integrated=True)  # Use integrated mode
        app.total_urls = len(folder_urls)  # Set the total number of URLs to process
        
        # Enqueue URLs for processing
        for url in folder_urls:
            app.enqueue_url(url)
        
        # Start the main event loop
        root.mainloop()

        # After the main loop exits, check if all songs are downloaded
        if app.downloaded_count == app.total_urls:
            print("All songs downloaded successfully")

    else:
        print("Folder not found or no URLs found in the specified folder.")

if __name__ == "__main__":
    main()
