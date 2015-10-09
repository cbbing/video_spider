# -*- coding: utf-8 -*-
#!/usr/bin/env python
#抓取响巢看看视频搜索结果
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


class KankanVideo(BaseVideo):
    def __init__(self):
        BaseVideo.__init__(self)
        self.engine = '响巢看看'
        self.general_url = 'http://search.kankan.com/search.php?keyword=keys' #普通搜索的url
        self.filePath = './data/kankan_video.xlsx'

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
            self.infoLogger.logger.info(encode_wrap('暂停%ds' % self.stop))
            print '\n'
            time.sleep(self.stop)


        #存入excel
        print len(self.dfs)
        self.data_to_excel()

    def search(self, key):

        fun_url = self.general_url
        fun_url = fun_url.replace('keys',key)

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
        driver.find_element_by_link_text('筛选').click()

        #普通

        #普通
        cf = ConfigParser.ConfigParser()
        cf.read("config.ini")
        lengthtypes = cf.get("kankan","lengthtype")
        lengthtypes = lengthtypes.strip('[').strip(']').split(',')
        for lengthtype in lengthtypes:

            try:
                buttonText = self.timelengthDict[int(lengthtype)]
                # 模拟点击
                driver.find_element_by_link_text(buttonText).click()

                self.infoLogger.logger.info(encode_wrap('%s, 第一页,暂停%ds' % (buttonText, self.stop)))
                print '\n'
                time.sleep(self.stop)

                #第一页
                self.parse_data(driver.page_source, 1, lengthtype)

                #获取下一页
                try:
                    for i in range(self.pagecount-1):
                        driver.find_element_by_link_text('下一页').click()

                        self.infoLogger.logger.info(encode_wrap('%s, 下一页:%d, 暂停%ds' % (buttonText,(i+2), self.stop)))
                        #print '*'*20, '%s, 下一页:%d, 暂停3s' % (buttonText,(i+2)), '*'*20
                        print '\n'
                        time.sleep(self.stop)

                        self.parse_data(driver.page_source, i+2, lengthtype)

                except Exception,e:
                    self.infoLogger.logger.info(encode_wrap('未达到%d页，提前结束' % self.pagecount))


            except Exception,e:
                self.errorLogger.logger.info(encode_wrap(str(e)))


        driver.quit()
        self.infoLogger.logger.info(encode_wrap('parse phantomjs success '))


    # 专辑搜索
    def parse_data_album(self, text):
        try:
            soup = bs(text)

            albumList = soup.findAll('ul', attrs={'class':'diversity_list diversity_list_zylist'})
            for album in albumList:

                #视频链接-专辑(样式一，如偶像来了等综艺节目）
                titleAndLinkList = album.findAll('a')
                for titleAndLink in titleAndLinkList:

                    try:
                        item = DataItem()

                        item.title = titleAndLink['title']
                        item.href = titleAndLink['href']

                        self.infoLogger.logger.info(encode_wrap('标题:%s' % item.title))
                        self.infoLogger.logger.info(encode_wrap('链接:%s' % item.href))

                        item.page = 1
                        item.durationType = '专辑'

                        self.items.append(item)
                    except Exception,e:
                        self.errorLogger.logger.info(encode_wrap( "专辑解析出错:%s" % str(e)))

        except Exception, e:
                print str(e)


    # 普通搜索
    def parse_data(self, text, page, lengthType):

        try:

            soup = bs(text)

            source = soup.find("ul", attrs={'class':'imglist imglist_150x85'})
            if source:
                titleAndLinks = source.findAll('a')

                #视频链接
                for titleAndLink in titleAndLinks:

                    if titleAndLink:
                        try:
                            item = DataItem()

                            item.title = titleAndLink['title']
                            item.href = titleAndLink['href']

                            self.infoLogger.logger.info(encode_wrap('标题:' + item.title))
                            self.infoLogger.logger.info(encode_wrap('链接:' + item.href))

                            durationTag = titleAndLink.find('span', attrs={'class':'masktxt'})
                            if durationTag:
                                self.infoLogger.logger.info(encode_wrap('时长:' + durationTag.text))
                                #print '时长:',durationTag.text
                                item.duration = durationTag.text

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

    data = pd.read_excel('keys.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
    print data

    video = KankanVideo()
    video.run(data['key'].get_values())

