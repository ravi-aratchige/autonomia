import pytest
from selenium import webdriver
from browser.driver import BrowserDriverManager


def test_driver_type():
    driver = BrowserDriverManager.get_driver()
    assert type(driver) == webdriver.Chrome
