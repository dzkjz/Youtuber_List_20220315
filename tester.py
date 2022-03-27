import os.path
from pprint import pprint
from Analyst.youtube_results_list_page import YoutubeResultsListPage
from Analyst.youtube_channel_page_analysis import YoutubeChannelPage
import re
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
import pickle
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
import undetected_chromedriver as uc
import random, time, os, sys
from selenium.webdriver.common.keys import Keys


# keyword = 'defi'
# headless = True
# random_ua = True
# youtube_results = YoutubeResultsListPage()
# youtube_results.Analysis(keywords=keyword, headless=headless, random_ua=random_ua)

# youtube_channel = YoutubeChannelPage()
#
# if os.path.exists("./Data/channels.txt"):
#     file = open("./Data/channels.txt")
#     urls = file.read()
#     urls = urls.splitlines()
#     for url in urls:
#         try:
#             youtube_channel.Analysis(channel_url=url, headless=True)
#         except:
#             print("报错")
#         finally:
#             continue


# str = """撒就是
# saksa
# saswdwdededww22
# sad brands@rachanaranade.in
# brands@rachanaranade.in 23"""
# email_regex = r"[\w\.-]+@[\w\.-]+"
# re_email = re.compile(email_regex, re.MULTILINE)
# emails_found = re_email.findall(str)
# print(emails_found)

def setDriver():
    # 服务初始值
    options = uc.ChromeOptions()

    # setting profile
    options.user_data_dir = "c:\\temp\\profile"

    # another way to set profile is the below (which takes precedence if both variants are used
    options.add_argument('--user-data-dir=c:\\temp\\profile2')

    # just some options passing in to skip annoying popups
    options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
    driver = uc.Chrome(options=options,
                       version_main=94)  # version_main allows to specify your chrome version instead of following chrome global version

    return driver


def save_cookies():
    # todo '''需要改动才用'''
    email = "dzkjzdzkjzdzkjz@gmail.com"
    password = "Dzkjz@123"

    driver = setDriver()
    driver.get("https://accounts.google.com/signin")
    email_phone = driver.find_element(By.XPATH, "//input[@id='identifierId']")
    email_phone.send_keys(email)
    driver.find_element(By.ID, "identifierNext").click()
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='password']")))
    password_ele = driver.find_element(By.XPATH, "//input[@name='password']")
    password_ele.send_keys(password)
    driver.find_element(By.ID, "passwordNext").click()
    time.sleep(5)

    google_cookies = driver.get_cookies()
    cookies = (
        {cookie.get("name"): cookie.get("value") for cookie in google_cookies}, google_cookies[0].get("expiry"))

    with open("cookies.pkl", "wb") as fd:
        pickle.dump(cookies, fd)

    return cookies


def testcode():
    GMAIL = '<GMAIL_HERE>'
    PASSWORD = '<PASSWORD_HERE>'

    chrome_options = uc.ChromeOptions()

    chrome_options.add_argument("--disable-extensions")

    chrome_options.add_argument("--disable-popup-blocking")

    chrome_options.add_argument("--profile-directory=Default")

    chrome_options.add_argument("--ignore-certificate-errors")

    chrome_options.add_argument("--disable-plugins-discovery")

    chrome_options.add_argument("--incognito")

    chrome_options.add_argument("user_agent=DN")

    driver = uc.Chrome(options=chrome_options)

    driver.delete_all_cookies()

    driver.get(
        "https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground&prompt=consent&response_type=code&client_id=407408718192.apps.googleusercontent.com&scope=email&access_type=offline&flowName=GeneralOAuthFlow")

    driver.find_element_by_xpath(
        "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input").send_keys(
        GMAIL)
    driver.find_element_by_xpath(
        "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input").send_keys(
        Keys.RETURN)

    time.sleep(10)

#
# cookies = save_cookies()
# print(cookies)
testcode()