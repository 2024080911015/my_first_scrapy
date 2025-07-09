import scrapy
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, \
    InvalidArgumentException
from selenium_stealth import stealth
import json
import requests

driver_path="C:/Users/iiijj/PycharmProjects/my_first_scrapy/chromedriver.exe"
service=Service(driver_path)
options=webdriver.ChromeOptions()
# options.add_argument("--headless")
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)
stealth(
    driver,
    languages="zh-CN",
    vendor="Google Inc.",
     platform="Win64",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)
driver.get("http://zhihu.com/signin")
input()
cookies=driver.get_cookies()
with open("zhihu_cookies.json","w") as f:
    json.dump(cookies,f)


