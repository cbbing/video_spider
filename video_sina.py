# -*- coding: utf-8 -*-
#!/usr/bin/env python
#抓取新浪视频搜索结果
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


class SinaVideo(BaseVideo):
    def __init__(self):
        BaseVideo.__init__(self)
        self.engine = '新浪'
        self.site = 'sina'
        self.general_url = 'http://so.video.sina.com.cn/s?wd=key' #普通搜索的url
        self.filePath = 'sina_video'
        self.timelengthDict = {0:'不限', 1:'0-10分钟', 2:'10-30分钟', 3:'30-60分钟', 4:'60分钟以上'} #时长类型对应网页中的按钮文字

        self.infoLogger = Logger(logname=dir_log+'info_sina(' + GetNowDate()+ ').log', logger='I')
        self.errorLogger = Logger(logname=dir_log+'error_sina(' + GetNowDate()+ ').log', logger='E')

    def run(self, keys):

        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        lengthtypes = cf.get("sina","lengthtype")
        if len(lengthtypes.strip('[').strip(']')) == 0:
            print encode_wrap('配置为不运行')
            return

        self.run_keys(keys)

        # for key in keys:
        #     try:
        #         # 初始化
        #         self.items = []
        #
        #         #搜索
        #         self.search(key)
        #
        #         #创建dataframe
        #         df = self.create_data(key)
        #
        #         self.data_to_sql_by_key(key, df)
        #
        #         self.infoLogger.logger.info(encode_wrap('暂停%ds' % self.stop))
        #         #print '*'*20, '暂停10s', '*'*20
        #         print '\n'
        #         time.sleep(self.stop)
        #
        #     except Exception,e:
        #         self.errorLogger.logger.info(key+'_unfinish_' + str(e))
        #         self.data_to_unfinish_file(self.web, key)
        #
        #
        # #保存数据
        # self.save_data()

    def search(self, key):

        qq_url = self.general_url
        qq_url = qq_url.replace('key',key)

        self.infoLogger.logger.info(encode_wrap('start phantomjs'))
        self.infoLogger.logger.info(encode_wrap(qq_url))
        #print 'start phantomjs'
        #print qq_url
        #driver = webdriver.PhantomJS()
        driver = webdriver.Firefox()
        driver.get(qq_url)

        # driver.get_screenshot_as_file("show.png")
        #
        # f = open('./data/data.html','w')
        # f.write(driver.page_source)
        # f.close()


        #普通
        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        lengthtypes = cf.get("sina","lengthtype")
        lengthtypes = lengthtypes.strip('[').strip(']').split(',')

        #展开“筛选”按钮
        try:
            driver.find_element_by_link_text("筛选").click()
            time.sleep(1)
        except Exception,e:
            self.infoLogger.logger.info(encode_wrap('无筛选按钮（没找到相关视频:%s）' % key))
            return

        for lengthtype in lengthtypes:

            try:
                buttonText = self.timelengthDict[int(lengthtype)]
                # 模拟点击
                #driver.find_element_by_xpath('//a[@node-value="1800000-3600000"]').click()
                driver.find_element_by_link_text(buttonText).click()

                driver.get_screenshot_as_file("show.png")

                self.infoLogger.logger.info(encode_wrap('%s, 第一页,暂停%ds' % (buttonText, self.stop)))
                #print '*'*20, '%s, 第一页,暂停3s' % buttonText, '*'*20
                print '\n'
                time.sleep(self.stop)

                #第一页
                self.parse_data(driver.page_source, 1, lengthtype)

                #获取下一页
                try:
                    for i in range(self.pagecount-1):
                        driver.find_element_by_link_text('下一页>').click()

                        self.infoLogger.logger.info(encode_wrap('%s, 下一页:%d, 暂停%ds' % (buttonText,(i+2)), self.stop))
                        #print '*'*20, '%s, 下一页:%d, 暂停3s' % (buttonText,(i+2)), '*'*20
                        print '\n'
                        time.sleep(self.stop)

                        driver.get_screenshot_as_file("show.png")
                        self.parse_data(driver.page_source, i+2, lengthtype)

                except Exception,e:
                    self.errorLogger.logger.error(encode_wrap('未达到%d页，提前结束' % self.pagecount))
                    #print '未达到%d页，提前结束' % self.pagecount


            except Exception,e:
                self.errorLogger.logger.error(encode_wrap(str(e)))
                #print str(e)

        driver.quit()
        print 'parse phantomjs success'


    # 普通搜索
    def parse_data(self, text, page, lengthType):

        soup = bs(text)

        sourceList = soup.findAll("li", attrs={'class':'SC_card'})
        for source in sourceList:
            titleAndLinkDiv = source.find('div', attrs={'class':'card_tit'})

            #视频链接
            if titleAndLinkDiv:

                try:

                    titleAndLink = titleAndLinkDiv.find('a')

                    item = DataItem()

                    self.infoLogger.logger.info(encode_wrap('标题:%s' % titleAndLink.get_text()))
                    self.infoLogger.logger.info(encode_wrap('链接:%s' % titleAndLink['href']))
                    #print '标题:',titleAndLink.get_text()
                    #print '链接:',titleAndLink['href']
                    item.title = titleAndLink.get_text()
                    item.href = titleAndLink['href']

                    durationTag = source.find('span', attrs={'class':'card_time'})
                    if durationTag:
                        self.infoLogger.logger.info(encode_wrap('时长:%s' % durationTag.text))
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
                    #print str(e)


if __name__=='__main__':
    #key = raw_input('输入搜索关键字:')

    data = pd.read_excel('keys.xlsx', 'Sheet2', index_col=None, na_values=['NA'])
    print data

    video = SinaVideo()
    video.run(data['key'].get_values())

