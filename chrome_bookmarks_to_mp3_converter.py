import customtkinter
from chrome_bookmarks_parser import ChromeBookmarksParser
from youtube_to_mp3_converter import YoutubeToMP3Converter

# Function to retrieve URLs from a specified folder using Chrome bookmarks
def process_folder_urls(folder_name):
    chrome_bookmarks_config_path = 'config.json'
    parser = ChromeBookmarksParser(chrome_bookmarks_config_path)
    folder_urls = parser.find_folder_urls(folder_name)
    return folder_urls

def main():
    # Prompt user to enter the name of the folder to process
    folder_name = input("Enter the name of the folder to process: ")
    
    # Retrieve URLs associated with the specified folder
    folder_urls = process_folder_urls(folder_name)

    if folder_urls:
        # If URLs are found in the folder, proceed with processing
        print("Found URLs in folder:", folder_urls)

        # Create a Tkinter root window
        root = customtkinter.CTk()

        # Initialize the YoutubeToMP3Converter application with integrated mode
        app = YoutubeToMP3Converter(root, integrated=True)

        # Set the total number of URLs to process
        app.total_urls = len(folder_urls)
        print(f"Preparing to download {app.total_urls} files")
        
        # Enqueue each URL for processing
        for url in folder_urls:
            app.enqueue_url(url)
        
        # Start the Tkinter main event loop
        root.mainloop()

        # After the main loop exits, check if all songs are downloaded
        if app.downloaded_count == app.total_urls:
            print("All songs downloaded successfully")

    else:
        # If no URLs are found, inform the user
        print("Folder not found or no URLs found in the specified folder.")

if __name__ == "__main__":
    main()
