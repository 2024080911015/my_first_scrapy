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
    try:
        view_all_button=driver.find_element(By.CSS_SELECTOR,".ViewAll-QuestionMainAction")
        view_all_button.click()
    except NoSuchElementException:
        pass
    for i in range(5000):
        print("正在进行第"+str(i+1)+"次滚动")
        try:
            read_moer_button=driver.find_element(By.CSS_SELECTOR,".ContentItem-more")
            read_moer_button.click()
        except NoSuchElementException:
            pass
        driver.execute_script("window.scrollBy(0,1000)")
        time.sleep(1)


class ZhihuScraperSpider(scrapy.Spider):
    name = "zhihu_scraper"
    #allowed_domains = ["www.zhihu.com"]
    start_urls = ["https://www.zhihu.com/question/575409863/answer/3577518284"]


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
