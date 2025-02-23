from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from scraper import scrape_uni_pages, scrape_unalm

import os

brave_path = os.getenv("BRAVE_PATH", "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe")
chromedriver_path = os.getenv("CHROMEDRIVER_PATH", "C:/Users/Maicol/.wdm/drivers/chromedriver/win64/133.0.6943.126/chromedriver.exe")

def main():
    service = Service(chromedriver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1240,720")
    options.add_argument("--disable-notifications")
    options.binary_location = brave_path

    with Chrome(service=service, options=options) as driver:
        #scrape_uni_pages(driver)
        scrape_unalm(driver)


if __name__ == "__main__":
    main()