# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import os.path
import time

from scrapy.http import HtmlResponse
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
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter



class MyFirstSpiderDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self):
        self.driver=None
        print("浏览器将在首次需要时启动")
    def _start_driver(self):
        if self.driver==None:
            driver_path="C:/Users/iiijj/PycharmProjects/my_first_scrapy/chromedriver.exe"
            service=Service(driver_path)
            options=webdriver.ChromeOptions()
            # options.add_argument("--headless")
            options.add_experimental_option("useAutomationExtension", False)
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            service = Service(driver_path)
            self.driver = webdriver.Chrome(service=service, options=options)
            stealth(
                self.driver,
                languages="zh-CN",
                vendor="Google Inc.",
                platform="Win64",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
            )

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        middleware = cls()
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        return middleware

    # MyFirstSpiderDownloaderMiddleware 类中的 process_request 方法

    def process_request(self, request, spider):
        # 从 request.meta 中获取 selenium_actions 列表
        actions = request.meta.get('selenium_actions')
        if not actions:
            return None

        # 将加载 cookie 的函数和其他函数分离开
        # 这里假设 load_cookies 是 actions 列表中的第一个函数
        cookie_action = None
        other_actions = []
        if actions and actions[0].__name__ == 'load_cookies':
            cookie_action = actions[0]
            other_actions = actions[1:]
        else:
            other_actions = actions

        self._start_driver()
        try:
            # 1. 先访问主域名，为设置 Cookie 创造环境
            print("正在访问主域名以设置Cookie...")
            self.driver.get("https://www.zhihu.com")

            # 2. 如果有 cookie_action，就执行它来加载 Cookie
            if cookie_action:
                print("正在应用Cookie...")
                cookie_action(self.driver)

            # 3. 现在，带着已加载的 Cookie 访问真正的目标网址
            print(f"正在导航至目标网址: {request.url}")
            self.driver.get(request.url)

            # (可选) 等待几秒，让页面有时间进行重定向或加载动态内容
            time.sleep(3)

            # 4. 执行所有其他操作，例如滚动
            print("正在执行页面滚动等其他操作...")
            if isinstance(other_actions, list):
                for action in other_actions:
                    action(self.driver)
            else:
                other_actions(self.driver)

            body = self.driver.page_source
            return HtmlResponse(
                url=self.driver.current_url,
                body=body,
                encoding='utf-8',
                request=request
            )
        except Exception as e:
            print(f"Selenium中间件发生错误: {e}")
            return None

    def spider_closed(self):
        if self.driver:
            self.driver.quit()
