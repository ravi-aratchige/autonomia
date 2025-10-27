import atexit
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Set extension path
EXTENSION_PATH = "../extension"


class BrowserDriverManager:
    _driver = None

    @staticmethod
    def get_driver():
        if BrowserDriverManager._driver is None:
            # Initialize ChromeOptions
            options = Options()

            # Set options to allow media device access
            options.add_argument("--use-fake-ui-for-media-stream")
            options.add_argument("--use-fake-device-for-media-stream")
            prefs = {"profile.default_content_setting_values.media_stream_mic": 1}
            options.add_experimental_option("prefs", prefs)

            # Set options to remove automation info bar
            # NOTE this is the "Chrome is being controlled by..." message
            options.add_experimental_option("excludeSwitches", ["enable-automation"])

            # Load unpacked extension into browser
            options.add_argument(f"--load-extension={EXTENSION_PATH}")

            # Initialize Chromedriver
            BrowserDriverManager._driver = webdriver.Chrome(options=options)

        return BrowserDriverManager._driver

    @staticmethod
    def quit_driver():
        if BrowserDriverManager._driver is not None:
            BrowserDriverManager._driver.quit()
            BrowserDriverManager._driver = None


# Ensure cleanup at exit
atexit.register(BrowserDriverManager().quit_driver)
