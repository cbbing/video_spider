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
from util.MyLogger import InfoLogger


class BaiduVideo(BaseVideo):
    def __init__(self):
        BaseVideo.__init__(self)
        self.engine = '百度'
        self.general_url = 'http://www.baidu.com/s?wd=key' #普通搜索的url
        self.filePath = './data/baidu_video.xlsx'
        self.timelengthDict = {0:'全部', 1:'10分钟以下', 2:'10-30分钟', 3:'30-60分钟', 4:'60分钟以上'} #时长类型对应网页中的按钮文字

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
            break

        #存入excel
        print len(self.dfs)
        self.data_to_excel()

    def search(self, key):

        #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))

        baidu_url = self.general_url
        baidu_url = baidu_url.replace('key',key)

        InfoLogger.addLog('start phantomjs')
        InfoLogger.addLog(baidu_url)
        #print 'start phantomjs'
        #print baidu_url

        #driver = webdriver.PhantomJS()
        driver = webdriver.Firefox()
        driver.get(baidu_url)

        driver.get_screenshot_as_file("show.png")

        f = open('./data/baidu.html','w')
        f.write(driver.page_source)
        f.close()

        #普通
        self.parse_data(driver.page_source, 1)

        for i in range(2, self.pagecount):
            # 模拟点击
            driver.find_element_by_link_text('下一页>').click()

            InfoLogger.addLog('%s, 第%d页' % (key, i))
            print '\n'
            #time.sleep(3)

            self.parse_data(driver.page_source, i)

        InfoLogger.addLog('stop phantomjs')

        driver.quit()


    # 普通搜索
    def parse_data(self, text, page):

        try:

            soup = bs(text)

            driver_each = webdriver.Firefox()

            sourceList = soup.findAll("h3", attrs={'class':'t'})
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
                        driver_each.get(item.href)
                        InfoLogger.addLog(driver_each.current_url)
                        item.href = driver_each.current_url

                        InfoLogger.addLog('标题:%s' % item.title)
                        InfoLogger.addLog('链接:%s' % item.href)

                        self.items.append(item)

                except Exception,e:
                    ErrorLogger.addLog(str(e))

            driver_each.quit()

        except Exception, e:
            ErrorLogger.addLog(str(e))


if __name__=='__main__':
    #key = raw_input('输入搜索关键字:')

    data = pd.read_excel('keys.xlsx', 'Sheet3', index_col=None, na_values=['NA'])
    print data

    video = BaiduVideo()
    video.run(data['key'].get_values())

