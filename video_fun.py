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
        self.site = 'fun'
        #self.album_url = 'http://www.fun.tv/search/?word=key'
        self.general_url = 'http://www.fun.tv/search/?word=key' #普通搜索的url
        self.filePath = 'fun_video'

        self.timelengthDict = {0:'全部', 1:'10分钟以下', 2:'10-30分钟', 3:'30-60分钟', 4:'60分钟以上'} #时长类型对应网页中的按钮文字

        #self.infoLogger = Logger(logname=dir_log+'info_fun(' + GetNowDate()+ ').log', logger='I')
        #self.errorLogger = Logger(logname=dir_log+'error_fun(' + GetNowDate()+ ').log', logger='E')

    @fn_timer_
    def run(self, keys):

        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        lengthtypes = cf.get("fun","lengthtype")
        if len(lengthtypes.strip('[').strip(']')) == 0:
            print encode_wrap('配置为不运行')
            return

        self.run_keys(keys)


    def search(self, key):

        items_all = []

        fun_url = self.general_url
        fun_url = fun_url.replace('key',key)

        #driver = webdriver.PhantomJS()
        driver = webdriver.Firefox()
        driver.get(fun_url)

        #driver.get_screenshot_as_file("show.png")

        # f = open('./data/data.html','w')
        # f.write(driver.page_source)
        # f.close()

        #专辑
        items = self.parse_data_album(driver.page_source, key)
        items_all.extend(items)

        # 模拟点击
        #driver.find_element_by_link_text('视频').click()


        #普通

        #第一页
        items = self.parse_data(driver.page_source, 1, 0, key)  #风行不支持时长选择，默认为0
        items_all.extend(items)

        #获取下一页
        try:
            for i in range(self.pagecount-1):
                driver.find_element_by_link_text('%d' % (i+2)).click()

                print '\n'
                #self.infoLogger.logger.info(encode_wrap('下一页:%d, 暂停%ds' % ((i+2), self.stop)))
                print encode_wrap('下一页:%d, 暂停%ds' % ((i+2), self.stop))
                print '\n'
                time.sleep(self.stop)

                driver.get_screenshot_as_file("show.png")

                items = self.parse_data(driver.page_source, i+2, 0, key)
                items_all.extend(items)

        except Exception,e:
            self.infoLogger.logger.info('未达到%d页，提前结束' % i)


        driver.quit()
        #self.infoLogger.logger.info(encode_wrap('parse phantomjs success '))

        return items_all

    # 专辑搜索
    def parse_data_album(self, text, key):
        items = []
        try:
            soup = bs(text, 'lxml')

            search_result = soup.find('div', {'class':'search-result'})
            more_result = soup.find('div', {'class':'morelist'})

            album_list = search_result.find_all('a', href=re.compile('^/subject/\d+'), title=re.compile('.+')) # 一般3个
            more_list = more_result.find_all('a', href=re.compile('^/vplay/g-\d+'), title=re.compile('.+')) # 更多
            album_list.extend(more_list)
            for album in album_list:

                item = DataItem()

                item.title = album['title']
                item.href = album['href']
                if not 'fun' in item.href:
                    item.href = 'http://www.fun.tv' + item.href

                print encode_wrap('标题:%s' % item.title)
                print encode_wrap('链接:%s' % item.href)

                item.page = 1
                item.durationType = '专辑'

                items.append(item)




        except Exception, e:
            self.errorLogger.logger.error( "%s: %s 专辑解析出错:%s" % (self.site, key, str(e)))

        return items

    # 普通搜索
    def parse_data(self, text, page, lengthType, key):

        items = []

        try:

            soup = bs(text, 'lxml')
            search_result = soup.find('div', {'class':'videolist'})
            search_list = search_result.find_all('a', href=re.compile('^/vplay/'), title=re.compile('.+')) # 更多


            #视频链接
            for titleAndLink in search_list:

                item = DataItem()

                item.title = titleAndLink['title']
                item.href = titleAndLink['href']

                if not 'fun' in item.href:
                    item.href = 'http://www.fun.tv' + item.href

                #self.infoLogger.logger.info(encode_wrap('标题:' + item.title))
                #self.infoLogger.logger.info(encode_wrap('链接:' + item.href))

                item.page = page
                try:
                    item.durationType = self.timelengthDict[int(lengthType)]
                except Exception,e:
                    print encode_wrap('未找到对应的时长类型!')

                items.append(item)

        except Exception, e:
            self.errorLogger.logger.error(self.site + ":"+key + ":" + str(e))

        return items

if __name__=='__main__':
    #key = raw_input('输入搜索关键字:')

    data = pd.read_excel('keys.xlsx', 'Sheet2', index_col=None, na_values=['NA'])
    print data

    video = FunVideo()
    video.run(data['key'].get_values())

