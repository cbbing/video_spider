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
from util.MyLogger import Logger
import platform
import requests



class BaiduVideo(BaseVideo):
    def __init__(self):
        BaseVideo.__init__(self)
        self.engine = '百度'
        #self.general_url = 'http://www.baidu.com/s?wd=key' #普通搜索的url
        self.general_url ='https://www.baidu.com/s?wd=key&pn=10&oq=key&tn=baiduhome_pg&ie=utf-8&usm=1&rsv_idx=3&rsv_pq=a15244ab000719f5&rsv_t=0e3d8UvmBPqha2nBnvxnGcRrOKKFbThEAimJjEkxffLDR1TONjuYOYAU7LEf5YAWeJx7'
        self.filePath = 'baidu_video'
        self.timelengthDict = {0:'全部', 1:'10分钟以下', 2:'10-30分钟', 3:'30-60分钟', 4:'60分钟以上'} #时长类型对应网页中的按钮文字

        self.infoLogger = Logger(logname=dir_log+'info_baidu.log', logger='I')
        self.errorLogger = Logger(logname=dir_log+'error_baidu.log', logger='E')


    def run(self, keys):
        for key in keys:
            # 初始化
            self.items = []

            #搜索
            self.search(key)
            #过滤
            #self.filter_short_video()
            #创建dataframe
            self.create_data(key)

            print '\n'
            print '*'*20, '暂停1s', '*'*20
            print '\n'
            time.sleep(1)


        #保存数据
        self.save_data()

    def search(self, key):

        #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))

        baidu_url = self.general_url
        baidu_url = baidu_url.replace('key',key)

        self.infoLogger.logger.info('start phantomjs')
        self.infoLogger.logger.info(baidu_url)
        #print 'start phantomjs'
        #driver = webdriver.PhantomJS()
        driver = webdriver.Firefox()
        driver.get(baidu_url)

        driver.get_screenshot_as_file("show.png")

        f = open('./data/baidu.html','w')
        f.write(driver.page_source)
        f.close()

        #普通
        self.parse_data(driver.page_source, 1)

        for i in range(2, self.pagecount+1):
            # 模拟点击
            driver.find_element_by_link_text('下一页>').click()
            #driver.get_screenshot_as_file("show.png")
            self.infoLogger.logger.info(encode_wrap('%s, 第%d页' % (key, i)))
            print '\n'
            #time.sleep(3)

            self.parse_data(driver.page_source, i)

        self.infoLogger.logger.info('stop phantomjs')

        driver.quit()


    # 普通搜索
    def parse_data(self, text, page):

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

                        self.infoLogger.logger.info(encode_wrap('标题:%s' % item.title))
                        self.infoLogger.logger.info(encode_wrap('链接:%s' % item.href))

                        self.items.append(item)

                except Exception,e:
                    self.errorLogger.logger.error(encode_wrap(str(e)))

            #driver_each.quit()

        except Exception, e:
            self.errorLogger.logger.error(encode_wrap(str(e)))

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

if __name__=='__main__':
    #key = raw_input('输入搜索关键字:')
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

    video = BaiduVideo()
    video.filePath = 'baidu_video'
    video.run(data['key'].get_values())

