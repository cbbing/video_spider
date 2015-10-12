# -*- coding: utf-8 -*-
#!/usr/bin/env python
#抓取风行视频搜索结果
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


class FunVideo(BaseVideo):
    def __init__(self):
        BaseVideo.__init__(self)
        self.engine = '风行'
        self.general_url = 'http://www.fun.tv/search/?word=key' #普通搜索的url
        self.filePath = './data/fun_video.xlsx'

        self.timelengthDict = {0:'全部', 1:'10分钟以下', 2:'10-30分钟', 3:'30-60分钟', 4:'60分钟以上'} #时长类型对应网页中的按钮文字

        self.infoLogger = Logger(logname='./data/log/info_fun.log', logger='I')
        self.errorLogger = Logger(logname='./data/log/error_fun.log', logger='E')


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
            self.infoLogger.logger.info(encode_wrap('暂停%ds' % self.stop))
            print '\n'
            time.sleep(self.stop)


        #存入excel
        print len(self.dfs)
        self.data_to_excel()

    def search(self, key):

        fun_url = self.general_url
        fun_url = fun_url.replace('key',key)

        self.infoLogger.logger.info(encode_wrap('start phantomjs'))
        self.infoLogger.logger.info(encode_wrap(fun_url))

        #driver = webdriver.PhantomJS()
        driver = webdriver.Firefox()
        driver.get(fun_url)

        driver.get_screenshot_as_file("show.png")

        f = open('./data/data.html','w')
        f.write(driver.page_source)
        f.close()

        #专辑
        self.parse_data_album(driver.page_source)

        # 模拟点击
        driver.find_element_by_link_text('视频').click()



        #普通

        #第一页
        self.parse_data(driver.page_source, 1, 0)  #风行不支持时长选择，默认为0

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


    # 专辑搜索
    def parse_data_album(self, text):
        try:
            soup = bs(text)

            albumList = soup.findAll('ul', attrs={'class':'torrent fix text'})
            for album in albumList:

                #视频链接-专辑(样式一，如偶像来了等综艺节目）

                titleAndLinkList = album.findAll('a')
                for titleAndLink in titleAndLinkList:

                    try:
                        item = DataItem()

                        item.title = titleAndLink['title']
                        item.href = titleAndLink['href']

                        if not 'fun' in item.href:
                            item.href = 'http://www.fun.tv/' + item.href


                        self.infoLogger.logger.info(encode_wrap('标题:%s' % item.title))
                        self.infoLogger.logger.info(encode_wrap('链接:%s' % item.href))

                        item.page = 1
                        item.durationType = '专辑'

                        self.items.append(item)
                    except Exception,e:
                        self.errorLogger.logger.info(encode_wrap( "专辑解析出错:%s" % str(e)))

        except Exception, e:
                self.errorLogger.logger.info(encode_wrap( "专辑解析出错:%s" % str(e)))


    # 普通搜索
    def parse_data(self, text, page, lengthType):

        try:

            soup = bs(text)

            source = soup.find("div", attrs={'class':'search-result'})
            if source:
                titleAndLinks = source.findAll('a')

                #视频链接
                for titleAndLink in titleAndLinks:

                    if titleAndLink:
                        try:
                            item = DataItem()

                            item.title = titleAndLink['title']
                            item.href = titleAndLink['href']

                            if not 'fun' in item.href:
                                item.href = 'http://www.fun.tv' + item.href

                            self.infoLogger.logger.info(encode_wrap('标题:' + item.title))
                            self.infoLogger.logger.info(encode_wrap('链接:' + item.href))

                            item.page = page
                            try:
                                item.durationType = self.timelengthDict[int(lengthType)]
                            except Exception,e:
                                self.errorLogger.logger.info(encode_wrap('未找到对应的时长类型!'))

                            self.items.append(item)

                        except Exception,e:
                            self.errorLogger.logger.info(encode_wrap(str(e)))


        except Exception, e:
            self.errorLogger.logger.info(encode_wrap(str(e)))


if __name__=='__main__':
    #key = raw_input('输入搜索关键字:')

    data = pd.read_excel('keys.xlsx', 'Sheet2', index_col=None, na_values=['NA'])
    print data

    video = FunVideo()
    video.run(data['key'].get_values())

