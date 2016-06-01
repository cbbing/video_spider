# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from util.webHelper import get_requests, get_web_driver
import time
import re
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from util.helper import fn_timer
from util.webHelper import get_requests

def check_404(url):
    """
    检测是否有无效链接
    """
    if 'fun.tv' in url or 'iqiyi.com' in url or 'sohu.com' in url:
        return check_404_by_selenium(url)
    else:
        return check_404_by_requests(url)

@fn_timer
def check_404_by_selenium(url, driver = None):
    """
    检测是否有无效链接
    :param date_start:
    :param date_end:
    :return:
    """
    #url = 'http://v.youku.com/v_show/id_XNjIyMzEwODU2.html?from=s1.8-1-1.2'
    try:
        p = re.compile('抱歉，您访问的页面不存在|'
                       '链接可能被删除或输入错误网址')

        if driver == None:
            driver = webdriver.Firefox()

        driver.get(url)
        data = driver.page_source
        driver.quit()

        soup = bs(data, 'lxml')
        # print soup.title.text
        if soup.title and '404' in soup.title.text:
            return False

        find = p.search(data)
        if find:
            print find.group()
            return False

    except Exception, e:
        print e

    return True

def check_404_by_requests(url):
    """
    检测是否有无效链接
    :param date_start:
    :param date_end:
    :return:
    """
    #url = 'http://v.youku.com/v_show/id_XNjIyMzEwODU2.html?from=s1.8-1-1.2'

    try:


        p = re.compile('该页面不存在|'
                       '您访问的页面在宇宙中失联|'
                       '该视频不存在|'
                       '对不起，您访问的视频暂时无法访问|'
                        '抱歉，您访问的页面不存在|'
                       'http://v.qq.com/error.html')

        print url
        r = get_requests(url, False)
        if 'charset=utf-8' in r.text:
            r.encoding='utf8'
        soup = bs(r.text, 'lxml')
        #print soup.title.text
        if soup.title and '404' in soup.title.text:
            return False
        elif 'error' in r.url or '404' in r.url or '503' in r.url or \
                'http://www.mgtv.com' == r.url or 'http://www.wasu.cn' == r.url:
            return False

        find = p.search(r.text)
        if find:
            print find.group()
            return False

        # elif ''

    except Exception, e:
        print "check404:",e

    return True


#print check_404('http://v.youku.com/v_show/id_XNjIyMzEwODU2.html?from=s1.8-1-1.2')
