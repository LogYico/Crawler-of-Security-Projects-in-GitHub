#Coding=UTF-8

from bs4 import BeautifulSoup
import requests
import pymysql
import random
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
'''
def UrlCrawler(pagenum):
    browser = webdriver.Chrome()
    browser.implicitly_wait(300)
    browser.get("https://github.com/topics/security")
    i = 0
    for i in range(0,pagenum):
        browser.find_element_by_class_name("ajax-pagination-btn btn btn-outline border-gray-dark f6 mt-0 width-full").click();


UrlCrawler(5)
'''


page = requests.Session()
securityUrl = "https://baidu.com"  # 获取安全类主题页面
mf = page.get(securityUrl)
msoup = BeautifulSoup(mf.content, "lxml")
print(len(msoup.find_all(class_='c3')))