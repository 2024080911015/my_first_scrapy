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

from my_first_spider.items import MyFirstSpiderItem


def scroll(driver):
    for i in range(50):
        print("正在进行第"+str(i+1)+"次滚动")
        driver.execute_script("window.scrollBy(0,300);")
        try:
            view_all_button=driver.find_element(By.CSS_SELECTOR,".mm_seemore")
            view_all_button.click()
        except NoSuchElementException:
            pass
        time.sleep(1)
class BingScraperSpider(scrapy.Spider):
    name = "bing_scraper"
    #allowed_domains = ["cn.bing.com"]
    start_urls = ["https://cn.bing.com/images/search?q=%E5%88%BB%E6%99%B4&form=HDRSC2&first=1","https://cn.bing.com/images/search?q=%E5%88%BB%E6%99%B4%E7%BE%8E%E5%9B%BE&qs=n&form=QBIRMH&sp=-1&lq=0&pq=%E5%88%BB%E6%99%B4mei&sc=10-5&cvid=F4FF8E597AA6455CAD4934757D2D13A2&first=1"]
    selenium_actions=[scroll]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                meta={'selenium_actions':self.selenium_actions},
                callback=self.parse
            )

    def parse(self, response):
        image_links=response.css(".mimg::attr(src)").getall()
        if image_links:
            print("找到"+str(len(image_links))+"个链接")
            item=MyFirstSpiderItem()
            item["image_urls"]=image_links
            yield item
        else:
            print("没有找到链接")
