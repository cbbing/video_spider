#!/usr/local/bin/python
#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import requests
import random
import ConfigParser
import pickle
import pandas as pd
import wrapcache

from retrying import retry
from selenium import webdriver
from selenium.webdriver.common.proxy import *

from code_convert import encode_wrap, GetNowDate
from sqlalchemy import create_engine
from helper import fn_timer

# 浏览器的窗口最大化
def max_window(driver, width_scale=1, height_scale=2):
    driver.maximize_window()
    siz = driver.get_window_size()
    driver.set_window_size(siz['width']*width_scale, siz['height']*height_scale)


@retry(stop_max_attempt_number=100)
def get_requests(url, has_proxy=True, cookie=None):
    """
    requests使用代理请求
    :param url:
    :param has_proxy:
    :param cookie:
    :return requests:
    """

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}

    proxy = None
    if has_proxy:
        proxy = get_proxies()
    # cf = ConfigParser.ConfigParser()
    # cf.read('../config.ini')
    # timeout = int(cf.get('web', 'timeout'))
    timeout = 5

    r = requests.get(url, proxies=proxy, headers=headers, cookies=cookie,timeout=timeout)
    output = 'Code:{1}  Proxy:{2}  Url:{0}  '.format(url, r.status_code, proxy)
    print encode_wrap(output)

    if int(r.status_code) != 200:
        raise Exception('request fail')

    return r

@retry(stop_max_attempt_number=100)
def get_session(url, has_proxy=True, cookie=None):
    """
    requests Session使用代理请求
    :param url:
    :param has_proxy:
    :param cookie:
    :return requests:
    """

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}

    proxy = None
    if has_proxy:
        proxy = get_proxies()
    cf = ConfigParser.ConfigParser()
    cf.read('../config.ini')
    timeout = int(cf.get('web', 'timeout'))

    s = requests.Session()
    r = s.get(url, proxies=proxy, headers=headers, cookies=cookie,timeout=timeout)
    output = 'Code:{0}  Proxy:{1}'.format(r.status_code, proxy)
    print encode_wrap(output)

    if int(r.status_code) != 200:
        raise Exception('request fail')

    return r, s


@retry(stop_max_attempt_number=100)
def get_web_driver(url=None, has_proxy=True, simulator='Firefox'):
    """
    Selenium 使用代理请求
    :param url:
    :param simulator:FireFox or PhantomJS
    :return driver:
    """

    def _get_driver():
        if has_proxy:
            proxies = get_proxies()
            if proxies.has_key('http'):
                myProxy = proxies['http']
            elif proxies.has_key('https'):
                myProxy = proxies['https']

            proxy = Proxy({
               'proxyType': ProxyType.MANUAL,
                'httpProxy': myProxy,
                # 'ftpProxy': myProxy,
                # 'sslProxy': myProxy,
                # 'noProxy':d ''
            })
            print encode_wrap("使用代理:"), myProxy
            if simulator == 'Firefox':
                driver = webdriver.Firefox(proxy=proxy)
            elif simulator == 'Chrome':
                driver = webdriver.Chrome()(proxy=proxy)
            else:
                driver = webdriver.PhantomJS(proxy=proxy)
        else:
            if simulator == 'Firefox':
                driver = webdriver.Firefox()
            elif simulator == 'Chrome':
                driver = webdriver.Chrome()()
            else:
                driver = webdriver.PhantomJS()


        return driver

    driver = _get_driver()
    #driver.set_page_load_timeout(30)
    if url:
        driver.get(url)

    return driver


@retry(stop_max_attempt_number=100)
def get_web_driver_phantomjs(url, has_proxy=True):
    """
    Selenium 使用代理请求
    :param url:
    :return driver:
    """

    if has_proxy:
        proxies = get_proxies()
        if proxies.has_key('http'):
            myProxy = proxies['http']
        elif proxies.has_key('https'):
            myProxy = proxies['https']

        proxy = Proxy({
           'proxyType': ProxyType.MANUAL,
            'httpProxy': myProxy,
            # 'ftpProxy': myProxy,
            # 'sslProxy': myProxy,
            # 'noProxy':d ''
        })
        print encode_wrap("使用代理:"), myProxy
        driver = webdriver.Chrome()(proxy=proxy)
    else:
        driver = webdriver.Chrome()()

    #driver.set_page_load_timeout(30)
    driver.get(url)

    return driver

from db_config import engine_ip
@wrapcache.wrapcache(timeout=60*60)  # 缓存1小时
def get_ip_dataframe():
    mysql_table_ip = 'ip_proxy'
    sql = 'select * from {0} where Speed > 0 order by Speed limit {1}'.format(mysql_table_ip, 1000)
    # sql = 'select * from ip_proxy_pay'
    df_ip = pd.read_sql_query(sql, engine_ip)
    return df_ip

# 获取IP代理地址(随机)
@fn_timer
def get_proxies():

    df_ip = get_ip_dataframe()

    if len(df_ip) > 0:

        index = random.randint(0, len(df_ip))
        print 'IP proxy length:{0}, Random Index:{1}'.format(len(df_ip), index)
        http = df_ip.ix[index, 'Type']
        http = str(http).lower()
        ip = df_ip.ix[index, 'IP']
        port = df_ip.ix[index, 'Port']
        ip_proxy = "%s://%s:%s" % (http, ip, port)
        proxies = {http:ip_proxy}
        return proxies
    else:
        return {}