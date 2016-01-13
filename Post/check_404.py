# -*- coding: utf-8 -*-

from util.webHelper import get_requests, get_web_driver
import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from util.helper import fn_timer

@fn_timer
def check_404(url):
    """
    检测是否有无效链接
    :param date_start:
    :param date_end:
    :return:
    """
    #url = 'http://v.youku.com/v_show/id_XNjIyMzEwODU2.html?from=s1.8-1-1.2'

    driver = webdriver.PhantomJS()

    driver.get(url)
    soup = bs(driver.page_source, 'lxml')
    driver.close()

    if '404' in soup.title.text:
        return True

    driver.close()
    return False



print check_404('http://v.youku.com/v_show/id_XNjIyMzEwODU2.html?from=s1.8-1-1.2')
