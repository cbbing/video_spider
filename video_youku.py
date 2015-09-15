# -*- coding: utf-8 -*-
#!/usr/bin/env python
#抓取优酷搜索结果
import sys
import time
import requests
import ConfigParser

from pandas import Series, DataFrame

from video_base import BaseVideo

reload(sys)
sys.setdefaultencoding("utf-8")


from bs4 import BeautifulSoup as bs
import pandas as pd
from video_base import *

class YoukuVideo(BaseVideo):
    def __init__(self):
        BaseVideo.__init__(self)
        self.engine = '搜酷'
        self.filePath = './data/youku_video.xlsx'

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

        cf = ConfigParser.ConfigParser()
        cf.read("config.ini")

        lengthtypes = cf.get("youku","lengthtype")
        lengthtypes = lengthtypes.strip('[').strip(']').split(',')
        for lengthtype in lengthtypes:

            for i in range(self.pagecount):
                youku_url = 'http://www.soku.com/search_video/q_key_orderby_1_lengthtype_%d?site=14&page=%d' % (lengthtype, i+1)
                youku_url = youku_url.replace('key',key)

                r = requests.get(youku_url)
                self.parse_data(r.text)


    def parse_data(self, text):
        soup = bs(text)

        #视频链接-专辑
        dramaList = soup.findAll('a', attrs={'class':'accordion-toggle collapsed'})
        for drama in dramaList:

            item = DataItem()

            print '标题:',drama['title']
            print '链接:',drama['href']
            item.title = drama['title']
            item.href = drama['href']

            self.items.append(item)


        #视频链接
        dramaList = soup.findAll('div', attrs={'class':'v-link'})
        for drama in dramaList:
            titleAndLink = drama.find('a')

            if titleAndLink:
                print '标题:',titleAndLink['title']
                print '链接:',titleAndLink['href']

                item = DataItem()
                item.title = titleAndLink['title']
                item.href = titleAndLink['href']
                self.items.append(item)
                # self.titles.append(titleAndLink['title'])
                # self.hrefs.append(titleAndLink['href'])

        # 视频时长
        dramaList = soup.findAll('div', attrs={'class':'v-thumb'})
        for drama in dramaList:
            titleAndImg = drama.findAll('img')

            if titleAndImg:
                print type(titleAndImg[0])
                print '标题:',titleAndImg[0]['alt']
                print '图片链接:',titleAndImg[0]['src']

                for item in self.items:
                    if item.title == titleAndImg[0]['alt']:
                        vTime = dramaList[0].findAll('div')
                        if len(vTime) > 3:
                            print len(vTime)
                            print '时长:',vTime[3].text
                            item.duration = vTime[3].text
                            break


if __name__=='__main__':
    #key = raw_input('输入搜索关键字:')

    data = pd.read_excel('快乐阳光-监测片单.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
    print data.columns

    youkuVideo = YoukuVideo()
    youkuVideo.run(data['key'].get_values())
    #youkuVideo.run(['偶像来了'])
    #key = '快乐大本营'
    #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))


