import random
import time
import os
from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *


class YoutubeResultsListPage:
    def __init__(self, max_scroll_times=100):
        '''设置最大下滚动页面次数20次'''
        self.__driver_options__ = webdriver.ChromeOptions()
        self.__driver__: webdriver = None
        self.__lang_list__ = ['ar-AE',
                              'ar-EG',
                              'ca-ES',
                              'cy-GB',
                              'da-DK',
                              'de-AT',
                              'de-CH',
                              'de-DE',
                              'de-LU',
                              'en-AU',
                              'en-CA',
                              'en-CA',
                              'en-CB',
                              'en-GB',
                              'en-SG',
                              'en-IE',
                              'en-NZ',
                              'en-PH',
                              'en-US',
                              'en-ZA',
                              'en-ZW',
                              'es-AR',
                              'es-VE',
                              'es-CR',
                              'es-MX',
                              'es-PR',
                              'es-ES',
                              'fr-BE',
                              'fr-CA',
                              'fr-CH',
                              'fr-FR',
                              'fr-LU',
                              'it-CH',
                              'it-IT',
                              'ko-KR',
                              'nl-BE',
                              'nl-NL',
                              'pt-BR',
                              'pt-PT',
                              'ru-RU',
                              'se-FI',
                              'se-SE',
                              'se-NO',
                              'ta-IN',
                              'th-TH',
                              'tr-TR',
                              'uk-UA',
                              'vi-VN',
                              'zh-CN',
                              'zh-HK',
                              'zh-MO',
                              'zh-SG',
                              'zh-TW',
                              'zu-ZA'
                              ]
        self.__ua_string__ = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
        self.__channel_xpath__ = '//*[@id="metadata"]//*[contains(@id,"channel")]//a[@class="yt-simple-endpoint style-scope yt-formatted-string"]'
        self.__hashtag_page_error_notice_xpath__ = '//*[@icon-name="hashtag-landing-page:HASHTAG_LANDING_PAGE_ERROR"]'
        self.__channel_file_path__ = "./Data/channels.txt"
        self.__keyword_file_path__ = './Data/keyword.txt'
        self.__channel_hrefs__ = []
        self.__max_scroll_times__ = max_scroll_times

    def randomize_user_agent(self):
        str = """
            Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
            Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0
            Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36
            Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
            Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36
            Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36
            Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15
            Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36
            Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0
            Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56
            Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 OPR/84.0.4316.21
            Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0
            Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0
            Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36
            Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15
            Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0
            Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36
            Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62
            Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15
            Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:97.0) Gecko/20100101 Firefox/97.0
            Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:97.0) Gecko/20100101 Firefox/97.0
            Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36
            Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36
            Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.3 Safari/605.1.15
            Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1
            Mozilla/5.0 (Linux; Android 11; Samsung SM-A025G) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19
            Mozilla/5.0 (Linux; Android 11; SM-A426U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36
            Mozilla/5.0 (Linux; Android 7.0; SM-G930VC Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36
            Mozilla/5.0 (Linux; Android 11; SM-M127N) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36
            Mozilla/5.0 (Linux; Android 11; SM-G998W) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36
            Mozilla/5.0 (Linux; Android 11; moto g(10) power Build/RRBS31.Q1-3-34-1-2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.105 Mobile Safari/537.36
            Mozilla/5.0 (Linux; Android 11; moto g(50) Build/RRFS31.Q1-59-76-2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.159 Mobile Safari/537.36 EdgW/1.0
            Mozilla/5.0 (Linux; Android 10; moto g play (2021)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36
            Mozilla/5.0 (Linux; Android 10; NOH-NX9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36
            Mozilla/5.0 (Linux; U; Android 10; zh-cn; BRQ-AN00 Build/HUAWEIBRQ-AN00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/11.9 Mobile Safari/537.36 COVC/045717
            Mozilla/5.0 (Linux; Android 11; Nokia G20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.88 Mobile Safari/537.36
            Mozilla/5.0 (Linux; Android 11; V2108) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36
            Mozilla/5.0 (Linux; Android 11; V2045) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36
            Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.111 Mobile Safari/537.36
            Mozilla/5.0 (Linux; Android 11; M2103K19PG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Mobile Safari/537.3
            Mozilla/5.0 (Linux; Android 11; M2102K1G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Mobile Safari/537.36
            Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/36.0  Mobile/15E148 Safari/605.1.15
            Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/36.0  Mobile/15E148 Safari/605.1.15
            Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/13.2b11866 Mobile/16A366 Safari/605.1.15
            Mozilla/5.0 (iPhone; CPU iPhone OS 14_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/92.0.4515.90 Mobile/15E148 Safari/604.1
            Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Mobile/15E148 Safari/604.1
            Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1
            Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1
            Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1
            Mozilla/5.0 (iPhone13,3; U; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/15E148 Safari/602.1 
            Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/13.2b11866 Mobile/16A366 Safari/605.1.15
            Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/36.0  Mobile/15E148 Safari/605.1.15
            Mozilla/5.0 (Linux; U; Android 4.0.4; ru-ru; SonyEricssonMT15iv Build/4.1.B.1.13) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30
            Mozilla/5.0 (Linux; U; Android 4.3; zh-tw; HTC_8160 Build/JSS15J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30
            Mozilla/5.0 (Linux; U; Android 2.1-update1; es-mx; SonyEricssonE10a Build/2.0.A.0.504) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 
            Mozilla/5.0 (Linux; U; Android 10; in-id; SM-M205G Build/QP1A.190711.020) AppleWebKit/533.1 (KHTML, like Gecko) Mobile Safari/533.1
            Mozilla/5.0 (Linux; Android 10; moto g(8) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/68 Safari/537.36
            Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4748.169 Safari/537.36 Edg/96.0.1039.25
            Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62
            Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.57
            Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36 Edg/96.0.1054.53
            """
        uas = str.splitlines()
        ua = random.choice(uas)
        ua = ua.strip()
        return ua

    def headless(self, headless):
        # 设置无头浏览器
        if headless:
            self.__driver_options__.add_argument('--headless')
            self.__driver_options__.add_argument('--disable-gpu')

    def ua(self):
        self.__ua_string__ = self.randomize_user_agent()
        self.__driver_options__.add_argument(f"--user-agent={self.__ua_string__}")
        print(f"使用ua： {self.__ua_string__}")

    def setDriver(self, headless=False, random_ua=False):
        # 设置headless模式
        self.headless(headless=headless)
        # 服务初始值
        service = ChromeService(executable_path=ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
        # 随机UA与否
        if random_ua:
            self.__ua_string__ = self.randomize_user_agent()
            self.ua()
        # 配置driver
        self.__driver__ = webdriver.Chrome(service=service, options=self.__driver_options__)

    def browserWaiter(self):

        wait = WebDriverWait(self.__driver__, 20, poll_frequency=1,
                             ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])
        wait.until(EC.presence_of_all_elements_located)
        page_state = ''
        try:
            page_state = self.__driver__.execute_script('return document.readyState;')
        finally:
            return page_state == 'complete'

    def openUrl(self, keywords, headless=False, random_ua=False):
        # 设置与初始化Driver
        self.setDriver(headless=headless, random_ua=random_ua)
        # 打开页面
        self.__driver__.get(f'https://www.youtube.com/hashtag/{keywords}')

        # 等待页面打开
        self.browserWaiter()

        # 检测页面打开是否正常
        loaded_hash_tag_page = self.checkIfHashTagPageLoaded()
        # hashtag打开有异常 跳到search page
        if not loaded_hash_tag_page:
            print("hashtag打开有异常 跳到search page")
            self.__driver__.get(f'https://www.youtube.com/results?search_query={keywords}')
            # 等待页面打开
            self.browserWaiter()

    def getChannels(self):

        # 获取channel
        channels: List[WebElement] = self.__driver__.find_elements(By.XPATH, self.__channel_xpath__)
        for channel in channels:
            channel_href = channel.get_attribute('href')
            if channel_href not in self.__channel_hrefs__:
                self.__channel_hrefs__.append(channel_href)

    def checkIfHashTagPageLoaded(self):
        state = True
        try:
            # 寻找异常提示元素
            WebDriverWait(self.__driver__, 10).until(
                EC.visibility_of_element_located((By.XPATH, self.__hashtag_page_error_notice_xpath__)))
            state = False
        finally:
            return state

    def Analysis(self, keywords, headless=False, random_ua=False):
        self.openUrl(keywords=keywords, headless=headless, random_ua=random_ua)

        SCROLL_PAUSE_TIME = 2
        i = 1
        while i < self.__max_scroll_times__:
            self.getChannels()
            # 保存数据
            self.txt_writer(self.__channel_file_path__, self.__channel_hrefs__)
            # 保存当前 keywords
            self.txt_writer(self.__keyword_file_path__, [keywords])
            if not self.scrollByCoord():
                break
            time.sleep(SCROLL_PAUSE_TIME)
            self.browserWaiter()
            i += 1
        # 退出浏览器
        self.__driver__.quit()

    def pageScrollDown(self):

        # Get scroll height
        last_height = self.__driver__.execute_script("return document.body.scrollHeight")
        # Scroll down to bottom
        self.__driver__.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scrollDwonByKey(self):
        element = self.__driver__.find_element(By.CSS_SELECTOR, '#spinner')
        element.location_once_scrolled_into_view()

    def nextChannelPages(self):
        loaded = False
        try:
            WebDriverWait(driver=self.__driver__, timeout=20, poll_frequency=1,
                          ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#spinner')))
            loaded = True
        finally:
            return loaded

    def scrollByCoord(self):
        if not self.nextChannelPages():
            return False
        element = self.__driver__.find_element(By.CSS_SELECTOR, '#spinner')
        desired_y = (element.size['height'] / 2) + element.location['y']
        window_h = self.__driver__.execute_script('return window.innerHeight')
        window_y = self.__driver__.execute_script('return window.pageYOffset')
        current_y = (window_h / 2) + window_y
        scroll_y_by = desired_y - current_y
        self.__driver__.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
        return True

    def infiniteScroll(self):
        SCROLL_PAUSE_TIME = 2
        # Get scroll height
        last_height = self.__driver__.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.__driver__.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.__driver__.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def txt_writer(self, path, urls: List):
        if not os.path.exists(path):
            print("不存在文件")
            f = open(path, "w+")
            f.close()

        # 读取文件
        textfile = open(path, "w+")
        for url in urls:
            # 循环
            old_urls = textfile.read().splitlines()  # 取过去的url
            if url not in old_urls:  # 判断去重,重复的不写入
                textfile.write(url + "\n")
        textfile.close()
