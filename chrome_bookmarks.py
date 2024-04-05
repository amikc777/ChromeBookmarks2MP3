from selenium import webdriver
import json

# Path to the Chrome profile directory
with open("config.json") as config_file:
            config = json.load(config_file)
            chrome_profile_path = config["chrome_profile_path"]

# Initialize the WebDriver with Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f'--user-data-dir={chrome_profile_path}')
chrome_options.add_argument('--profile-directory=Default')  # Specify the default profile directory

try:
    # Initialize the WebDriver with Chrome options
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the desired webpage
    driver.get("https://www.google.com")

    # Keep the script running indefinitely to prevent the browser window from closing
    input("Press Enter to close the browser...")

except Exception as e:
    print("An error occurred:", e)
    input("Press Enter to exit...")
