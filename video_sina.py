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
from util.MyLogger import InfoLogger, ErrorLogger

class SinaVideo(BaseVideo):
    def __init__(self):
        BaseVideo.__init__(self)
        self.engine = '新浪'
        self.general_url = 'http://so.video.sina.com.cn/s?wd=key' #普通搜索的url
        self.filePath = './data/sina_video.xlsx'
        self.timelengthDict = {0:'不限', 1:'0-10分钟', 2:'10-30分钟', 3:'30-60分钟', 4:'60分钟以上'} #时长类型对应网页中的按钮文字

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

            InfoLogger.addLog('暂停10s')
            #print '*'*20, '暂停10s', '*'*20
            print '\n'
            time.sleep(10)
            break

        #存入excel
        print len(self.dfs)
        self.data_to_excel()

    def search(self, key):

        qq_url = self.general_url
        qq_url = qq_url.replace('key',key)

        InfoLogger.addLog('start phantomjs')
        InfoLogger.addLog(qq_url)
        #print 'start phantomjs'
        #print qq_url
        #driver = webdriver.PhantomJS()
        driver = webdriver.Firefox()
        driver.get(qq_url)

        driver.get_screenshot_as_file("show.png")

        f = open('./data/sina.html','w')
        f.write(driver.page_source)
        f.close()


        #普通
        cf = ConfigParser.ConfigParser()
        cf.read("config.ini")
        lengthtypes = cf.get("sina","lengthtype")
        lengthtypes = lengthtypes.strip('[').strip(']').split(',')

        #展开“筛选”按钮
        driver.find_element_by_link_text("筛选").click()
        time.sleep(1)

        for lengthtype in lengthtypes:

            try:
                buttonText = self.timelengthDict[int(lengthtype)]
                # 模拟点击
                #driver.find_element_by_xpath('//a[@node-value="1800000-3600000"]').click()
                driver.find_element_by_link_text(buttonText).click()

                driver.get_screenshot_as_file("show.png")

                InfoLogger.addLog('%s, 第一页,暂停3s' % buttonText)
                #print '*'*20, '%s, 第一页,暂停3s' % buttonText, '*'*20
                print '\n'
                time.sleep(3)

                #第一页
                self.parse_data(driver.page_source)

                #获取下一页
                try:
                    for i in range(self.pagecount-1):
                        driver.find_element_by_link_text('下一页>').click()

                        InfoLogger.addLog('%s, 下一页:%d, 暂停3s' % (buttonText,(i+2)))
                        #print '*'*20, '%s, 下一页:%d, 暂停3s' % (buttonText,(i+2)), '*'*20
                        print '\n'
                        time.sleep(3)

                        driver.get_screenshot_as_file("show.png")
                        self.parse_data(driver.page_source)

                except Exception,e:
                    ErrorLogger.addLog('未达到%d页，提前结束' % self.pagecount)
                    #print '未达到%d页，提前结束' % self.pagecount


            except Exception,e:
                ErrorLogger.addLog(str(e))
                #print str(e)

        print 'parse phantomjs success'


    # 普通搜索
    def parse_data(self, text):

        soup = bs(text)

        sourceList = soup.findAll("li", attrs={'class':'SC_card'})
        for source in sourceList:
            titleAndLinkDiv = source.find('div', attrs={'class':'card_tit'})

            #视频链接
            if titleAndLinkDiv:

                try:

                    titleAndLink = titleAndLinkDiv.find('a')

                    item = DataItem()

                    InfoLogger.addLog('标题:%s' % titleAndLink.get_text())
                    InfoLogger.addLog('链接:%s' % titleAndLink['href'])
                    #print '标题:',titleAndLink.get_text()
                    #print '链接:',titleAndLink['href']
                    item.title = titleAndLink.get_text()
                    item.href = titleAndLink['href']

                    durationTag = source.find('span', attrs={'class':'card_time'})
                    if durationTag:
                        InfoLogger.addLog('时长:',durationTag.text)
                        #print '时长:',durationTag.text
                        item.duration = durationTag.text

                    self.items.append(item)

                except Exception,e:
                    ErrorLogger.addLog(str(e))
                    #print str(e)

if __name__=='__main__':
    #key = raw_input('输入搜索关键字:')

    data = pd.read_excel('keys.xlsx', 'Sheet2', index_col=None, na_values=['NA'])
    print data

    video = SinaVideo()
    video.run(data['key'].get_values())

