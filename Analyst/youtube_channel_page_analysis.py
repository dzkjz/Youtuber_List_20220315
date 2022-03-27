import random
import string
import time
import json
import re
from urllib import parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from Data.Youtuber import Youtuber


class YoutubeChannelPage:

    def __init__(self, keyword):
        self.__driver_options__ = webdriver.ChromeOptions()
        self.__driver__: webdriver = None
        self.__lang_list__ = [
            'en-US',
        ]
        self.__keyword__ = keyword
        self.__youtuber__ = Youtuber()
        self.__lang__ = None
        self.__ua_string__ = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
        self.__channel_subscribers_count_css__ = '#meta #subscriber-count'
        self.__channel_name_xpath__ = '//div[@id="contentContainer"]//*[@id="text-container"]//*[@id="text"]'
        self.__channel_location_xpath__ = '//span[contains(text(),"Location") or contains(text(),"位置")]/parent::yt-formatted-string/parent::td/following-sibling::td/yt-formatted-string'
        self.__channel_view_email_button_xpath__ = '//*[contains(text(),"View email address")]/parent::*[@id="button"]/parent::a'  # need recaptcha
        self.__channel_view_email_button_need_signin_xpath__ = '//div[@id="details-container"]//a[contains(text(),"Sign in") or contains(text(),"登陆") or contains(text(),"登录")]'  # need recaptcha
        self.__channel_description_text_css__ = '#description-container #description'  # regex get email address,sample:https://www.youtube.com/c/LookAround2020/about
        self.__channel_facebook_xpath__ = '//a[contains(@href,"facebook") and contains(@href,"youtube")]'
        self.__channel_twitter_xpath__ = '//a[contains(@href,"twitter") and contains(@href,"youtube")]'
        self.__channel_instagram_xpath__ = '//a[contains(@href,"instagram") and contains(@href,"youtube")]'
        self.__channel_other_contacts_xpath__ = '''//a[contains(@href,"event") and contains(@href,"youtube") and not(contains(@href,"facebook")) 
        and not(contains(@href,"twitter")) and not(contains(@href,"instagram"))]'''

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

    def lang(self):
        # 切换语言
        if self.__lang__ is None:
            lang_list = self.__lang_list__
            self.__lang__ = random.choice(lang_list).strip()

    def ua(self):
        self.__ua_string__ = self.randomize_user_agent()
        self.__driver_options__.add_argument(f"--user-agent={self.__ua_string__}")
        print(f"使用ua： {self.__ua_string__}")

    def setDriver(self, headless=False, random_ua=False):
        # 设置headless模式
        self.headless(headless=headless)
        # 设置语言
        self.lang()
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
            time.sleep(3)
            return page_state == 'complete'

    def openUrl(self, channel_url, headless=False, random_ua=False):
        # 设置与初始化Driver
        self.setDriver(headless=headless, random_ua=random_ua)
        # 打开页面
        url = f'{channel_url}/about'
        self.__driver__.get(url)
        print(url)
        # 等待页面打开
        self.browserWaiter()

    def getChannelSubscribers(self):
        subscriber_text_value = 0
        try:
            subscriber_text_element = self.__driver__.find_element(By.CSS_SELECTOR,
                                                                   self.__channel_subscribers_count_css__)
            subscriber_text_value_attr = 'aria-label'
            subscriber_text_value = subscriber_text_element.get_attribute(subscriber_text_value_attr)
            if str(subscriber_text_value).lower() == 'none':
                subscriber_text_value = '0'
                return subscriber_text_value
            if len(subscriber_text_value) > 1:
                if 'K' in subscriber_text_value:
                    subscriber_text_value = subscriber_text_value.replace('K subscribers', '')
                    subscriber_text_value = float(subscriber_text_value.strip()) * 1000
                elif '订阅' in subscriber_text_value and '万' in subscriber_text_value:
                    subscriber_text_value = subscriber_text_value.replace('万位订阅者', '')
                    subscriber_text_value = float(subscriber_text_value.strip()) * 10000
                elif '订阅' in subscriber_text_value and ',' in subscriber_text_value:
                    subscriber_text_value = subscriber_text_value.replace('位订阅者', '')
                    subscriber_text_value = subscriber_text_value.replace(',', '')
                    subscriber_text_value = float(subscriber_text_value.strip())
                elif '订阅' in subscriber_text_value and ',' not in subscriber_text_value:
                    subscriber_text_value = subscriber_text_value.replace('位订阅者', '')
                    subscriber_text_value = float(subscriber_text_value.strip())
                elif 'subscriber' in subscriber_text_value:
                    subscriber_text_value = subscriber_text_value.replace('subscribers', '').replace('subscriber', '')
                    if 'million' in subscriber_text_value:
                        subscriber_text_value = subscriber_text_value.replace('million', '')
                        subscriber_text_value = float(subscriber_text_value.strip()) * 1000000
                    subscriber_text_value = float(subscriber_text_value.strip())
                else:
                    subscriber_text_value = float(subscriber_text_value.strip())
        except NoSuchElementException:
            subscriber_text_value = '0'
        finally:
            subscriber_text_value = str(subscriber_text_value).replace('.0', '')
            return subscriber_text_value

    def getChannelName(self):
        try:
            name_text_element = self.__driver__.find_element(By.XPATH, self.__channel_name_xpath__)
            name_text_value = name_text_element.text
            name_text_value = name_text_value.strip()

        except NoSuchElementException:
            name_text_value = 'hidden'
        return name_text_value

    def getChannelLocation(self):
        try:
            location_text_element = self.__driver__.find_element(By.XPATH, self.__channel_location_xpath__)
            location_text_value = location_text_element.text
            location_text_value = location_text_value.strip()

        except NoSuchElementException:
            location_text_value = 'hidden'
        return location_text_value

    def getChannelSocialContact(self, variable_name):
        social_elements_value = []
        try:
            social_elements = self.__driver__.find_elements(By.XPATH,
                                                            getattr(self, f'__channel_{variable_name}_xpath__'))
            for social_element in social_elements:
                social_element_value = social_element.get_attribute('href')
                fixer_re = re.search(r"\&q\=(.*)", social_element_value)
                if fixer_re.group().count('http') > 0:
                    url_got = fixer_re.group(0).replace("&q=", "")
                    url_decode = parse.unquote(url_got)
                    if url_decode not in social_elements_value:
                        social_elements_value.append(url_decode)
        finally:
            return social_elements_value

    def getChannelEmailLink(self):
        channel_email_view_link = ''

        try:
            channel_email = self.__driver__.find_element(By.XPATH,
                                                         self.__channel_view_email_button_need_signin_xpath__)
            channel_email_view_link = channel_email.get_attribute('href')
        finally:
            return channel_email_view_link

    def getChannelEmailAddress(self):
        try:
            channel_email_element = self.__driver__.find_element(By.XPATH, self.__channel_view_email_button_xpath__)
            channel_email_element.click()
            # 对接打码
        except NoSuchElementException:
            print(NoSuchElementException.args)

    def getChannelEmailFromDetails(self, details):
        emails_found = []
        if len(details) > 0:
            # email_regex_1 = r"\S+@\S+"
            email_regex = r"[\w\.-]+@[\w\.-]+"
            re_email = re.compile(email_regex, re.MULTILINE)
            emails_found = re_email.findall(details)
        return emails_found

    def getChannelDetails(self):
        channel_detail = ''
        try:
            channel_detail_element = self.__driver__.find_element(By.CSS_SELECTOR,
                                                                  self.__channel_description_text_css__)
            channel_detail = channel_detail_element.text

        finally:
            return channel_detail

    def Analysis(self, channel_url, headless=False, random_ua=False):
        self.openUrl(channel_url=channel_url, headless=headless, random_ua=random_ua)

        # 获取subscriber数量
        subscribers_count = self.getChannelSubscribers()
        # 设置youtuber的subscriber数量
        self.__youtuber__.set_subscribers_count(subscribers_count)

        # 获取location
        location = self.getChannelLocation()
        # 设置youtuber的地区
        self.__youtuber__.set_location(location)

        # 获取name
        channel_name = self.getChannelName()
        # 设置name
        self.__youtuber__.set_channel_name(channel_name)
        # 设置url
        self.__youtuber__.set_channel_url(channel_url)

        # 获取 社交媒体联系方式
        elements = ['twitter', 'facebook', 'instagram', 'other_contacts']
        for element in elements:
            elements_value = self.getChannelSocialContact(variable_name=element)
            # json构造值
            elements_value = json.dumps(elements_value)
            # 设置值
            if element == 'twitter':
                self.__youtuber__.set_twitter(elements_value)
            elif element == 'facebook':
                self.__youtuber__.set_facebook(elements_value)
            elif element == 'instagram':
                self.__youtuber__.set_instagram(elements_value)
            elif element == 'other_contacts':
                self.__youtuber__.set_other_social(elements_value)
        # 获取email
        emailLink = self.getChannelEmailLink()
        self.__youtuber__.set_email_view_link(emailLink)
        # 获取details
        details = self.getChannelDetails()
        self.__youtuber__.set_description(details)
        if len(details) > 0:
            # 尝试解析Email regex
            email = self.getChannelEmailFromDetails(details)
            email = json.dumps(email)
            self.__youtuber__.set_email(email)
        # keyword
        self.__youtuber__.set_channel_source_keyword(self.__keyword__)
        # 保存数据
        self.__youtuber__.save_to_excel()
        # 退出浏览器
        self.__driver__.quit()
