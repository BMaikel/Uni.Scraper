from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service

from scraper import _page_uni

brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
chromedriver_path = "C:/Users/Maicol/.wdm/drivers/chromedriver/win64/133.0.6943.126/chromedriver.exe"

def main():
    service = Service(chromedriver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1240,720")
    options.add_argument("--disable-notifications")
    options.binary_location = brave_path
    driver = Chrome(service = service, options = options)

    _page_uni(driver)

if __name__ == "__main__":
    main()