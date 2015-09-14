# -*- coding: utf-8 -*-
#!/usr/bin/env python
#抓取乐视搜索结果
import sys
import time
import requests
from pandas import Series, DataFrame

reload(sys)
sys.setdefaultencoding("utf-8")

from bs4 import BeautifulSoup as bs
import pandas as pd
from pandas import Series, DataFrame
from selenium import webdriver
from video_base import BaseVideo


class LetvVideo(BaseVideo):
    def __init__(self):
        BaseVideo.__init__(self)
        self.engine = '乐视'
        self.filePath = './data/letv_video.xlsx'


    def run(self, keys):
        for key in keys:
            # 初始化
            self.items = []

            #搜索
            self.search(key)
            #过滤
            self.filter_short_video()
            #创建dataframe
            self.create_data(key)

            print '\n'*2
            print '*'*20, '暂停10s', '*'*20
            print '\n'*2
            time.sleep(10)
            break

        #存入excel
        print len(self.dfs)
        self.data_to_excel()

    def search(self, key):

        #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))
        letv_url = 'http://so.letv.com/s?wd=key&from=pc&index=0&ref=click'
        letv_url = letv_url.replace('key',key)
        letv_url = 'http://so.letv.com/s?wd=%E8%8A%B1%E5%84%BF%E4%B8%8E%E5%B0%91%E5%B9%B4&from=pc&index=0&ref=click'

        print 'start phantomjs'
        driver = webdriver.PhantomJS()
        driver.get(letv_url)



        self.parse_data(driver.page_source)

        # f = open('data.html','w')
        # f.write(driver.page_source)
        # f.close()

        for i in range(1, self.pagecount):
            driver.find_element_by_link_text("下一页").click();#点击链接
            print 'page %d : wait for 2s...' % (i+1)
            time.sleep(2)
            print 'after 2s...'
            self.parse_data(driver.page_source)


        print 'parse phantomjs success'


    def parse_data(self, text):
        # print text
        # f = open(r'./data/letv.html','r')
        # #f.write(text)
        # text = f.read()
        # f.close()

        try:

            soup = bs(text)

            sourceListAll = soup.findAll("ul", attrs={'class':'supplier-tab j-tui-tab'})
            for drama in sourceListAll:
                source = drama.find('a')

                name = source.get_text()
                print name

            #视频链接
            dramaList = soup.findAll('dl', attrs={'class':'w180'})
            for drama in dramaList:

                item = DataItem()

                titleAndLink = drama.find('a')
                if titleAndLink:
                    print '标题:',titleAndLink['title']
                    print '链接:',titleAndLink['href']
                    item.title = titleAndLink['title']
                    item.href = titleAndLink['href']
                durationTag = drama.find('b', attrs={'class':'tmbg'})
                if durationTag:
                    print '时长:',durationTag.text
                    item.duration = durationTag.text

                self.items.append(item)

        except Exception, e:
            print str(e)


class DataItem:
    def __init__(self):
        self.title = ''
        self.href = ''
        self.duration = ''

if __name__=='__main__':
    #key = raw_input('输入搜索关键字:')

    data = pd.read_excel('快乐阳光-监测片单.xlsx', 'Sheet1', index_col=None, na_values=['NA'])


    video = LetvVideo()
    video.run(data['key'].get_values())
    #video.search('key')
    #video.parse_data('')
    #key = '快乐大本营'
    #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))

    # driver = webdriver.PhantomJS()
    # driver.get('http://www.baidu.com')
    # data = driver.find_element_by_id('cp').text
    # print driver.page_source
