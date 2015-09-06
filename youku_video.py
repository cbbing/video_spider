# -*- coding: utf-8 -*-
#!/usr/bin/env python
#抓取优酷搜索结果
import sys
import time
import requests
from pandas import Series, DataFrame

reload(sys)
sys.setdefaultencoding("utf-8")

from bs4 import BeautifulSoup as bs

class YoukuVideo:
    def __init__(self):
        self.titles = []
        self.hrefs = []

    def search(self, key):

        for i in range(1,10):
            youku_url = "http://www.soku.com/search_video/q_key_orderby_1?site=14&page=%d" % i
            youku_url = youku_url.replace('key',key)

            r = requests.get(youku_url)
            self.parse_data(r.text)


    def parse_data(self, text):
        soup = bs(text)

        # 视频概略
        # dramaList = soup.findAll('div', attrs={'class':'v-thumb'})
        # dramaItems = []
        #
        # if(dramaList):
        #     titleAndImg = dramaList[0].findAll('img')
        #
        #     if titleAndImg:
        #         print type(titleAndImg[0])
        #         print '标题:',titleAndImg[0]['alt']
        #         print '图片链接:',titleAndImg[0]['src']
        #
        #     vTime = dramaList[0].findAll('div')
        #     if len(vTime) > 3:
        #         print len(vTime)
        #         print '时长:',vTime[3].text

        #视频链接
        dramaList = soup.findAll('div', attrs={'class':'v-link'})
        titles = []
        hrefs = []

        for drama in dramaList:
            titleAndLink = drama.find('a')

            if titleAndLink:
                print '标题:',titleAndLink['title']
                print '链接:',titleAndLink['href']
                self.titles.append(titleAndLink['title'])
                self.hrefs.append(titleAndLink['href'])



    def save_to_csv(self, key):
        df = DataFrame({'Title':self.titles, 'Href':self.hrefs}, columns=['Title', 'Href'])
        df['Time'] = self.getNowTime()
        df['Source'] = '优酷'
        print df[:10]
        df.to_csv('./data/youku_video_%s.csv' % key, encoding='utf-8', index=False)

    def getNowTime(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

if __name__=='__main__':
    key = raw_input('输入搜索关键字:')
    #key = '快乐大本营'
    #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))
    youkuVideo = YoukuVideo()
    youkuVideo.search(key)
    youkuVideo.save_to_csv(key)
