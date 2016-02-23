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
        self.site = 'letv'
        self.general_url = 'http://so.letv.com/s?wd=key' #普通搜索的url
        self.filePath = 'letv_video'

        self.timelengthDict = {0:'全部', 1:'10分钟以下', 2:'10-30分钟', 3:'30-60分钟', 4:'60分钟以上'} #时长类型对应网页中的按钮文字

        #self.infoLogger = Logger(logname=dir_log+'info_letv(' + GetNowDate()+ ').log', logger='I')
        #self.errorLogger = Logger(logname=dir_log+'error_letv(' + GetNowDate()+ ').log', logger='E')

    @fn_timer_
    def run(self, keys):

        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        lengthtypes = cf.get("letv","lengthtype")
        if len(lengthtypes.strip('[').strip(']')) == 0:
            print encode_wrap('配置为不运行')
            return

        self.run_keys(keys)


    def search(self, key):

        items_all = []

        letv_url = self.general_url
        letv_url = letv_url.replace('key',key)

        #self.infoLogger.logger.info(encode_wrap('start phantomjs'))
        #self.infoLogger.logger.info(encode_wrap(letv_url))

        #driver = webdriver.PhantomJS()
        driver = webdriver.Chrome()
        driver.get(letv_url)

        # driver.get_screenshot_as_file("show.png")
        #
        # f = open('./data/data.html','w')
        # f.write(driver.page_source)
        # f.close()

        #专辑
        items = self.parse_data_album(driver.page_source)
        items_all.extend(items)

        #普通
        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        lengthtypes = cf.get("letv","lengthtype")
        lengthtypes = lengthtypes.strip('[').strip(']').split(',')
        for lengthtype in lengthtypes:

            try:
                buttonText = self.timelengthDict[int(lengthtype)]
                # 模拟点击
                driver.find_element_by_link_text('播放时长').click()
                driver.find_element_by_link_text(buttonText).click()

                #driver.get_screenshot_as_file("show.png")

                #self.infoLogger.logger.info(encode_wrap('%s, 第一页,暂停%ds' % (buttonText, self.stop)))
                print encode_wrap('%s, 第一页,暂停%ds' % (buttonText, self.stop))
                print '\n'
                time.sleep(self.stop)

                #第一页
                items = self.parse_data(driver.page_source, 1, lengthtype)
                items_all.extend(items)

                #获取下一页
                try:
                    for i in range(self.pagecount-1):
                        driver.find_element_by_link_text('下一页').click()

                        #self.infoLogger.logger.info(encode_wrap('%s, 下一页:%d, 暂停%ds' % (buttonText,(i+2), self.stop)))
                        print encode_wrap('%s, 下一页:%d, 暂停%ds' % (buttonText,(i+2), self.stop))
                        print '\n'
                        time.sleep(self.stop)

                        driver.get_screenshot_as_file("show.png")

                        items = self.parse_data(driver.page_source, i+2, lengthtype)
                        items_all.extend(items)

                except Exception,e:
                    infoLogger.logger.info('未达到%d页，提前结束' % self.pagecount)


            except Exception,e:
                errorLogger.logger.error(str(e))


        driver.quit()
        #self.infoLogger.logger.info(encode_wrap('parse phantomjs success '))

        return items_all

    # 专辑搜索
    def parse_data_album(self, text):

        items = []

        try:
            soup = bs(text, 'lxml')
            albumList = soup.findAll('h1')
            for album in albumList:
                a = album.find('a')
                if not a:
                    continue

                item = DataItem()
                item.title = a['title']
                item.href = a['href']
                item.page = 1
                item.durationType = '专辑'

                if 'http' not in item.href:
                    continue

                items.append(item)

        except Exception, e:
                print str(e)

        return items


    # 普通搜索
    def parse_data(self, text, page, lengthType):

        items = []

        try:

            soup = bs(text, 'lxml')

            source = soup.find("div", attrs={'class':'wrap-body'})
            if source:
                titleAndLinks = source.findAll('a')

                #视频链接
                for titleAndLink in titleAndLinks:
                    try:

                        if titleAndLink:

                            item = DataItem()

                            #self.infoLogger.logger.info(encode_wrap('标题:' + titleAndLink['title']))
                            #self.infoLogger.logger.info(encode_wrap('链接:' + titleAndLink['href']))

                            item.title = titleAndLink['title']
                            item.href = titleAndLink['href']

                            durationTag = titleAndLink.find('b', attrs={'class':'tmbg'})
                            if durationTag:
                                #self.infoLogger.logger.info(encode_wrap('时长:' + durationTag.text))
                                item.duration = durationTag.text

                            item.page = page
                            try:
                                item.durationType = self.timelengthDict[int(lengthType)]
                            except Exception,e:
                                None
                                #self.errorLogger.logger.error(encode_wrap('未找到对应的时长类型!'))

                            items.append(item)

                    except Exception,e:
                        errorLogger.logger.error(str(e))


        except Exception, e:
            errorLogger.logger.error(str(e))

        return items

if __name__=='__main__':
    #key = raw_input('输入搜索关键字:')

    data = pd.read_excel('keys.xlsx', 'Sheet2', index_col=None, na_values=['NA'])
    print data

    video = LetvVideo()
    video.run(data['key'].get_values())

