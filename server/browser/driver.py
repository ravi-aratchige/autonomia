import atexit
from selenium import webdriver


class BrowserDriverManager:
    _driver = None

    @staticmethod
    def get_driver():
        if BrowserDriverManager._driver is None:
            BrowserDriverManager._driver = webdriver.Chrome()
        return BrowserDriverManager._driver

    @staticmethod
    def quit_driver():
        if BrowserDriverManager._driver is not None:
            BrowserDriverManager._driver.quit()
            BrowserDriverManager._driver = None


# Ensure cleanup at exit
atexit.register(BrowserDriverManager().quit_driver)
