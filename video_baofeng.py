# -*- coding: utf-8 -*-
#!/usr/bin/env python
#抓取暴风影音视频搜索结果
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


class BaofengVideo(BaseVideo):
    def __init__(self):
        BaseVideo.__init__(self)
        self.engine = '暴风影音'
        self.general_url = 'http://www.baofeng.com/q_key' #普通搜索的url
        self.filePath = './data/baofeng_video.xlsx'

        #self.timelengthDict = {0:'全部', 1:'10分钟以下', 2:'10-30分钟', 3:'30-60分钟', 4:'60分钟以上'} #时长类型对应网页中的按钮文字
        self.infoLogger = Logger(logname='./data/log/info_baofeng.log', logger='I')
        self.errorLogger = Logger(logname='./data/log/error_baofeng.log', logger='E')


    def run(self, keys):
        for key in keys:
            # 初始化
            self.items = []

            #搜索
            self.search(key)

            #创建dataframe
            self.create_data(key)

            print '\n'
            self.infoLogger.logger.info(encode_wrap('暂停%ds' % self.stop))
            print '\n'
            time.sleep(self.stop)


        #存入excel
        print len(self.dfs)
        self.data_to_excel()

    def search(self, key):

        fun_url = self.general_url
        fun_url = fun_url.replace('key',key)

        self.infoLogger.logger.info('start phantomjs')
        self.infoLogger.logger.info(fun_url)

        #driver = webdriver.PhantomJS()
        driver = webdriver.Firefox()
        driver.get(fun_url)

        driver.get_screenshot_as_file("show.png")

        f = open('./data/data.html','w')
        f.write(driver.page_source)
        f.close()

        #普通
        #第一页
        self.parse_data(driver.page_source, 1, 0)  #暴风不支持时长选择，默认为0

        #获取下一页
        try:
            for i in range(self.pagecount-1):
                driver.find_element_by_link_text('下一页').click()

                print '\n'
                self.infoLogger.logger.info(encode_wrap('下一页:%d, 暂停%ds' % ((i+2), self.stop)))
                print '\n'
                time.sleep(self.stop)

                driver.get_screenshot_as_file("show.png")

                self.parse_data(driver.page_source, i+2, 0)

        except Exception,e:
            self.infoLogger.logger.info(encode_wrap('未达到%d页，提前结束' % self.pagecount))


        driver.quit()
        self.infoLogger.logger.info(encode_wrap('parse phantomjs success '))


    # 普通搜索
    def parse_data(self, text, page, lengthType):

        try:

            soup = bs(text)

            source = soup.find("div", attrs={'class':'search-video-list'})
            if source:
                titleAndLinks = source.findAll('a')

                #视频链接
                for titleAndLink in titleAndLinks:

                    if titleAndLink:
                        try:
                            item = DataItem()

                            item.title = titleAndLink['title']
                            item.href = titleAndLink['href']

                            if not 'baofeng' in item.href:
                                item.href = 'http://www.baofeng.com' + item.href

                            self.infoLogger.logger.info(encode_wrap('标题:' + item.title))
                            self.infoLogger.logger.info(encode_wrap('链接:' + item.href))

                            durationTag = titleAndLink.find('span', attrs={'class':'search-video-time'})
                            if durationTag:
                                self.infoLogger.logger.info(encode_wrap('时长:' + durationTag.text))
                                #print '时长:',durationTag.text
                                item.duration = durationTag.text

                            item.page = page
                            try:
                                item.durationType = self.timelengthDict[int(lengthType)]
                            except Exception,e:
                                self.errorLogger.logger.error(encode_wrap('未找到对应的时长类型!'))

                            self.items.append(item)

                        except Exception,e:
                            self.errorLogger.logger.error(encode_wrap(str(e)))


        except Exception, e:
            self.errorLogger.logger.error(encode_wrap(str(e)))
            print str(e)

if __name__=='__main__':
    #key = raw_input('输入搜索关键字:')

    data = pd.read_excel('keys.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
    print data

    video = BaofengVideo()
    video.run(data['key'].get_values())

