# -*- coding: utf-8 -*-
#!/usr/bin/env python
#抓取腾讯视频搜索结果
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


class LetvVideo(BaseVideo):
    def __init__(self):
        BaseVideo.__init__(self)
        self.engine = '乐视'
        self.general_url = 'http://so.letv.com/s?wd=key' #普通搜索的url
        self.filePath = 'letv_video'

        self.timelengthDict = {0:'全部', 1:'10分钟以下', 2:'10-30分钟', 3:'30-60分钟', 4:'60分钟以上'} #时长类型对应网页中的按钮文字

        self.infoLogger = Logger(logname='./data/log/info_letv.log', logger='I')
        self.errorLogger = Logger(logname='./data/log/error_letv.log', logger='E')


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


        #保存数据
        self.save_data()

    def search(self, key):

        #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))

        letv_url = self.general_url
        letv_url = letv_url.replace('key',key)

        self.infoLogger.logger.info(encode_wrap('start phantomjs'))
        self.infoLogger.logger.info(encode_wrap(letv_url))

        #driver = webdriver.PhantomJS()
        driver = webdriver.Firefox()
        driver.get(letv_url)

        driver.get_screenshot_as_file("show.png")

        f = open('./data/data.html','w')
        f.write(driver.page_source)
        f.close()

        #专辑
        self.parse_data_album(driver.page_source)

        # 模拟点击
        driver.find_element_by_link_text('播放时长').click()

        #普通
        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        lengthtypes = cf.get("letv","lengthtype")
        lengthtypes = lengthtypes.strip('[').strip(']').split(',')
        for lengthtype in lengthtypes:

            try:
                buttonText = self.timelengthDict[int(lengthtype)]
                # 模拟点击
                driver.find_element_by_link_text(buttonText).click()

                driver.get_screenshot_as_file("show.png")

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

                        driver.get_screenshot_as_file("show.png")

                        self.parse_data(driver.page_source, i+2, lengthtype)

                except Exception,e:
                    self.infoLogger.logger.info(encode_wrap('未达到%d页，提前结束' % self.pagecount))


            except Exception,e:
                self.errorLogger.logger.error(encode_wrap(str(e)))


        driver.quit()
        self.infoLogger.logger.info(encode_wrap('parse phantomjs success '))


    # 专辑搜索
    def parse_data_album(self, text):
        try:
            soup = bs(text)

            albumList = soup.findAll('ul', attrs={'class':'zongyi_ul j-play-list'})
            for album in albumList:

                driver_each = webdriver.Firefox()

                #视频链接-专辑(样式一，如偶像来了等综艺节目）
                try:
                    titleAndLinkList = album.findAll('a')
                    for titleAndLink in titleAndLinkList:

                        item = DataItem()

                        item.title = titleAndLink.get_text()
                        item.href = titleAndLink['href']

                        if not 'letv' in item.href:
                            item.href = 'http://so.letv.com/' + item.href

                        #链接转真实url
                        driver_each.get(item.href)
                        time.sleep(3)
                        self.infoLogger.logger.info(encode_wrap(driver_each.current_url))
                        item.href = driver_each.current_url

                        self.infoLogger.logger.info(encode_wrap('标题:%s' % item.title))
                        self.infoLogger.logger.info(encode_wrap('链接:%s' % item.href))

                        item.page = 1
                        item.durationType = '专辑'

                        self.items.append(item)
                except Exception,e:
                    self.errorLogger.logger.error(encode_wrap( "专辑解析出错:%s" % str(e)))

                driver_each.quit()

            #视频链接-片花
            albumList = soup.findAll('div', attrs={'class':'list j-play-list'})
            for album in albumList:

                try:
                    dramaList = album.findAll('dd', attrs={'class':'d-t'})
                    for drama in dramaList:

                        titleAndLink = drama.find('a')
                        item = DataItem()

                        self.infoLogger.logger.info(encode_wrap('标题:' + titleAndLink['title']))
                        self.infoLogger.logger.info(encode_wrap('链接:' + titleAndLink['href']))
                        item.title = titleAndLink['title']
                        item.href = titleAndLink['href']

                        item.page = 1
                        item.durationType = '花絮'

                        self.items.append(item)

                except Exception, e:
                    self.errorLogger.logger.error(encode_wrap("片花解析出错" + str(e)))
                    #print "片花解析出错", str(e)

        except Exception, e:
                print str(e)


    # 普通搜索
    def parse_data(self, text, page, lengthType):

        try:

            soup = bs(text)

            source = soup.find("div", attrs={'class':'wrap-body'})
            if source:
                titleAndLinks = source.findAll('a')

                #视频链接
                for titleAndLink in titleAndLinks:
                    try:

                        if titleAndLink:

                            item = DataItem()

                            self.infoLogger.logger.info(encode_wrap('标题:' + titleAndLink['title']))
                            self.infoLogger.logger.info(encode_wrap('链接:' + titleAndLink['href']))

                            item.title = titleAndLink['title']
                            item.href = titleAndLink['href']

                            durationTag = titleAndLink.find('b', attrs={'class':'tmbg'})
                            if durationTag:
                                self.infoLogger.logger.info(encode_wrap('时长:' + durationTag.text))
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


if __name__=='__main__':
    #key = raw_input('输入搜索关键字:')

    data = pd.read_excel('keys.xlsx', 'Sheet2', index_col=None, na_values=['NA'])
    print data

    video = LetvVideo()
    video.run(data['key'].get_values())

