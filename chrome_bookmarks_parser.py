import json
import os

class ChromeBookmarksParser:
    """
    Parses Chrome bookmarks data to extract URLs from a specified folder.

    Parameters:
    - chrome_bookmarks_config_path: Path to the configuration file for Chrome bookmarks
    """
    def __init__(self, chrome_bookmarks_config_path):
        self.chrome_bookmarks_config_path = chrome_bookmarks_config_path
        self.load_config()


    def load_config(self):
        """
        Loads the configuration data from the specified Chrome bookmarks config file.
        """
        with open(self.chrome_bookmarks_config_path, 'r') as config_file:
            self.config = json.load(config_file)
        

    def find_folder_urls(self, folder_name):
        """
        Finds URLs within a specified folder in Chrome bookmarks.

        Parameters:
        - folder_name: Name of the folder to search for within Chrome bookmarks.

        Returns:
        - List of URLs found within the specified folder.
        """
        bookmarks_file_path = self.config.get('chrome_profile_path')
        if not bookmarks_file_path:
            print("Chrome bookmarks file path not found in the config.")
            return []
        
        if not bookmarks_file_path.endswith('.json'):
            bookmarks_file_path = os.path.join(bookmarks_file_path, 'Bookmarks')

        if not os.path.exists(bookmarks_file_path):
            print(f"Bookmarks file not found at {bookmarks_file_path}.")
            return []
        
        bookmarks_data = self.load_bookmarks(bookmarks_file_path)
        return self._find_folder_urls_recursive(bookmarks_data['roots']['bookmark_bar'], folder_name)
    

    def load_bookmarks(self, bookmarks_file_path):
        """
        Loads Chrome bookmarks data from the specified file path.

        Parameters:
        - bookmarks_file_path: Path to the Chrome bookmarks file.

        Returns:
        - Parsed JSON data representing Chrome bookmarks.
        """
        with open(bookmarks_file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    

    def _find_folder_urls_recursive(self, node, folder_name):
        """
        Recursively searches for URLs within a specified folder node.

        Parameters:
        - node: Current node to search for URLs.
        - folder_name: Name of the folder to search for.

        Returns:
        - List of URLs found within the specified folder node.
        """
        urls = []
        if 'children' in node:
            for child in node['children']:
                if child.get('name') == folder_name:
                    urls.extend(self._get_urls_from_node(child))
                elif child.get('children'):
                    urls.extend(self._find_folder_urls_recursive(child, folder_name))
        return urls
    
    
    def _get_urls_from_node(self, node):
        """
        Extracts URLs from a given node in the Chrome bookmarks data.

        Parameters:
        - node: Node from which to extract URLs.

        Returns:
        - List of URLs extracted from the node.
        """
        urls = []
        if node.get('type') == 'url':
            urls.append(node['url'])
        elif 'children' in node:
            for child in node['children']:
                urls.extend(self._get_urls_from_node(child))
        return urls


if __name__ == "__main__":
    chrome_bookmarks_config_path = 'config.json'
    parser = ChromeBookmarksParser(chrome_bookmarks_config_path)

    folder_name = input("Enter the name of the folder to process: ")
    folder_urls = parser.find_folder_urls(folder_name)

    if folder_urls:
        print("Found URLs in folder:", folder_urls)
        # Integrate with YoutubeToMP3Converter class for processing
    else:
        print("Folder not found or no URLs found in the specified folder.")
