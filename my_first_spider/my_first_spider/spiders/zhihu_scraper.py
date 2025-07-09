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


def load_cookies(driver):
    path="C:/Users/iiijj/PycharmProjects/my_first_scrapy/my_first_spider/zhihu_cookies.json"
    with open(path,"r") as f:
        cookies=json.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)
def scroll(driver):
    for i in range(50):
        print("正在进行第"+str(i+1)+"次滚动")
        try:
            read_moer_button=driver.find_element(By.CSS_SELECTOR,".ContentItem-more")
            read_moer_button.click()
        except NoSuchElementException:
            pass
        driver.execute_script("window.scrollBy(0,50)")
        time.sleep(1)


class ZhihuScraperSpider(scrapy.Spider):
    name = "zhihu_scraper"
    #allowed_domains = ["www.zhihu.com"]
    start_urls = ["https://www.zhihu.com/search?type=content&q=%E5%88%BB%E6%99%B4%E5%9B%BE%E7%89%87", "https://www.zhihu.com/search?type=content&q=%E5%8D%A1%E8%8A%99%E5%8D%A1", "https://www.zhihu.com/search?q=%E6%B5%81%E8%90%A4%E5%9B%BE%E7%89%87&search_source=History&utm_content=search_history&type=content", "https://www.zhihu.com/search?type=content&q=%E4%BA%8C%E6%AC%A1%E5%85%83%E7%BE%8E%E5%B0%91%E5%A5%B3%E5%9B%BE%E7%89%87"]


    selenium_actions=[load_cookies,scroll]
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                meta={'selenium_actions':self.selenium_actions},
                callback=self.parse
            )
    def parse(self, response):
        all_links=response.css('img::attr(src)').getall()
        valid_image_links = []
        for link in all_links:
            # 确保链接不是空的，并且是以 http 开头
            if link and link.startswith('http'):
                valid_image_links.append(link)

        # 3. 如果清洗后还有有效的链接，再创建 Item
        if valid_image_links:
            print(f"找到 {len(all_links)} 个总链接，其中有效链接 {len(valid_image_links)} 个")
            item = MyFirstSpiderItem()
            item['image_urls'] = valid_image_links
            yield item
        else:
            print("没找到任何有效的图片链接")
