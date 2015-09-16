# -*- coding: utf-8 -*-
#!/usr/bin/env python
#抓取优酷搜索结果
import sys
import time
import requests
import ConfigParser
import re
from video_base import *
from bs4 import BeautifulSoup as bs
import pandas as pd


reload(sys)
sys.setdefaultencoding("utf-8")




class SokuVideo(BaseVideo):
    def __init__(self):
        BaseVideo.__init__(self)
        self.engine = '搜酷'
        self.album_url = '' #专辑的url
        self.general_url = '' #普通搜索的url

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

        # 专辑
        album_url = self.album_url.replace('key',key)
        r = requests.get(album_url)
        self.parse_data_album(r.text)

        print '*'*20, '暂停10s', '*'*20
        print '\n'
        time.sleep(10)

        lengthtypes = cf.get("youku","lengthtype")
        lengthtypes = lengthtypes.strip('[').strip(']').split(',')
        for lengthtype in lengthtypes:

            for i in range(self.pagecount):
                soku_url = self.general_url.replace('tid', lengthtype)
                soku_url = self.general_url.replace('pid', str(i+1))
                soku_url = soku_url.replace('key',key)

                r = requests.get(soku_url)
                self.parse_data(r.text)

                print '*'*20, '暂停10s, key:%s, Page %d, 时长Type:%s' % (key, i+1, lengthtype), '*'*20
                print '\n'
                time.sleep(10)
                break

    # 专辑
    def parse_data_album(self, text):
        soup = bs(text)

        #视频链接-专辑
        dramaList = soup.findAll('a', attrs={'class':'accordion-toggle collapsed'})
        for drama in dramaList:

            item = DataItem()

            try:
                print '标题:',drama['title']
                print '链接:',drama['href']

                # 2015-09-16， 搜库专辑链接变动了！
                m = re.search(r"url=(.*?)&", drama['href'])
                href = m.group(1)

                item.title = drama['title']
                item.href = href

                self.items.append(item)

            except Exception, e:
                print str(e)


    # 普通
    def parse_data(self, text):
        soup = bs(text)

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
                #print '图片链接:',titleAndImg[0]['src']

                for item in self.items:
                    if item.title == titleAndImg[0]['alt']:
                        vTime = dramaList[0].findAll('div')
                        if len(vTime) > 3:
                            print len(vTime)
                            print '时长:',vTime[3].text
                            item.duration = vTime[3].text
                            break


if __name__=='__main__':

    data = pd.read_excel('keys.xlsx', 'Sheet2', index_col=None, na_values=['NA'])
    print data.columns

    youkuVideo = SokuVideo()
    youkuVideo.run(data['key'].get_values())
    #youkuVideo.run(['明若晓溪','旋风少女','偶像来了'])
    #key = '快乐大本营'
    #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))


