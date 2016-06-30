# -*- coding: utf-8 -*-
#!/usr/bin/env python
#抓取baidu搜索结果
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import time
import urllib
from bs4 import BeautifulSoup as bs
import pandas as pd
import ConfigParser
from pandas import Series, DataFrame
from selenium import webdriver
from video_base import *
from selenium.webdriver.support.ui import WebDriverWait
# from util.MyLogger import Logger
import platform
import requests
#from retrying import retry


class BaiduVideo(BaseVideo):
    def __init__(self):
        BaseVideo.__init__(self)
        self.engine = '百度'
        self.site = 'baidu'
        #self.general_url = 'http://www.baidu.com/s?wd=key' #普通搜索的url
        self.general_url ='https://www.baidu.com/s?wd=keys&pn=pid&oq=keys&tn=you2000_pg&ie=utf-8&usm=1&rsv_idx=2&rsv_pq=f00436260001bee1&rsv_t=38345vNGL%2FdXnHErSWuLY7Gj3Q2KpwF5L6yEDopbLycRLwSgO%2BuKTqX7nnK8un93tA'
        self.filePath = 'baidu_video'
        self.timelengthDict = {0:'全部', 1:'10分钟以下', 2:'10-30分钟', 3:'30-60分钟', 4:'60分钟以上'} #时长类型对应网页中的按钮文字

        # infoLogger = Logger(logname=dir_log+'info_baidu(' + GetNowDate()+ ').log', logger='I')
        # errorLogger = Logger(logname=dir_log+'error_baidu(' + GetNowDate()+ ').log', logger='E')


    @fn_timer_
    def run(self, keys):
        #self.run_keys(keys)
        self.run_keys_multithreading(keys)


    def search(self, key):

        items_all = []

        #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))


        baidu_url = self.general_url.replace('keys',key).replace('pid','0')

        r = self.get_requests(baidu_url)

        #普通
        items = self.parse_data(r.text, 1)
        items_all.extend(items)

        baidu_url = self.general_url.replace('keys',key)
        for i in range(1, self.pagecount):

            url = baidu_url.replace('pid','{}0'.format(i))
            r = self.get_requests(url)

            #普通
            items = self.parse_data(r.text, i+1)
            items_all.extend(items)



        #self.infoLogger.logger.info('stop phantomjs')



        return items_all


    # 普通搜索
    def parse_data(self, text, page):

        items = []

        try:

            soup = bs(text, 'html5lib')
            #print text
            sourceList = soup.findAll("h3")
            #sourceList = soup.findAll("div", attrs={'class':'content_left'})
            #print 'class="h3"' in text

            #driver_each = webdriver.Firefox()

            for source in sourceList:
                titleAndLink = source.find('a')

                #视频链接
                try:

                    if titleAndLink:

                        item = DataItem()
                        item.page = page

                        item.title = titleAndLink.get_text()
                        item.href = titleAndLink['href']

                        #百度链接转真实url
                        print item.href
                        originalURL = self.get_baidu_real_url(item.href)
                        print originalURL
                        item.href = originalURL
                        # driver_each.get(item.href)
                        #
                        # #过滤无效视频
                        # if 'error' in driver_each.current_url:
                        #     continue
                        # if '好像不能看了' in driver_each.page_source:
                        #     continue

                        #self.infoLogger.logger.info(encode_wrap(driver_each.current_url))
                        #item.href = driver_each.current_url

                        #self.infoLogger.logger.info(encode_wrap('标题:%s' % item.title))
                        #self.infoLogger.logger.info(encode_wrap('链接:%s' % item.href))

                        items.append(item)

                except Exception,e:
                    errorLogger.logger.error(self.site + ":" + str(e))

            #driver_each.quit()

        except Exception, e:
            errorLogger.logger.error(self.site + ":" + str(e))

        return items

    def get_baidu_real_url(self, url):
        tmpPage = requests.get(url, allow_redirects=False)
        if tmpPage.status_code == 200:
            urlMatch = re.search(r'URL=\'(.*?)\'', tmpPage.text.encode('utf-8'), re.S)
            originalURL = urlMatch.group(1)
        elif tmpPage.status_code == 302:
            originalURL = tmpPage.headers.get('location')
        else:
            originalURL = url
            print 'No URL found!!'
        return originalURL

    def run_auto(self):
        systemName = platform.system()
        if systemName == 'Windows':
            key_path = 'D:\Data\keys-baidu.xlsx'
            dir_path = 'D:/Data/Result/'
        else:
            key_path = 'keys-baidu.xlsx'
            dir_path = './data/'

        data = pd.read_excel(key_path, 'Sheet1', index_col=None, na_values=['NA'])
        print data
        if len(data) == 0:
            print 'no key, program will exit in 3s...'
            time.sleep(3)
            sys.exit(1)


        self.filePath = 'baidu_video'
        self.run(data['key'].get_values())

def run_baidu():
    video = BaiduVideo()
    video.run_auto()

if __name__=='__main__':
    #key = raw_input('输入搜索关键字:')
    run_baidu()


