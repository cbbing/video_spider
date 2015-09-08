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

class IQiYiVideo():
    def __init__(self):
        self.dfs = []
        self.titles = []
        self.hrefs = []
        self.items = []

    def run(self, keys):
        for key in keys:
            # 初始化
            self.titles = []
            self.hrefs = []

            #搜索
            self.search(key)
            #创建dataframe
            self.create_data(key)


        #存入excel
        print len(self.dfs)
        self.data_to_excel()

    def search(self, key):

        for i in range(1,11):
            iqiyi_url = "http://so.iqiyi.com/so/q_key_ctg__t_0_page_%d_p_1_qc_0_rd__site__m_1_bitrate_" % i
            iqiyi_url = iqiyi_url.replace('key',key)

            r = requests.get(iqiyi_url)
            self.parse_data(r.text)


    def parse_data(self, text):
        soup = bs(text)

        #视频链接
        dramaList = soup.findAll('a', attrs={'class':'figure  figure-180101 '})


        for drama in dramaList:

            item = DataItem()

            titleAndLink = drama.find('img')
            if titleAndLink:
                print '标题:',titleAndLink['title']
                print '链接:',drama['href']#titleAndLink['href']
                item.title = titleAndLink['title']
                item.href = drama['href']
            durationTag = drama.find('span', attrs={'class':'v_name'})
            if durationTag:
                item.duration = durationTag.text

            self.items.append(item)

    def create_data(self, key):
        df = DataFrame({'Title':[item.title for item in self.items], 'Href':[item.href for item in self.items], 'Duration':[item.duration for item in self.items]}, columns=['Title', 'Href', 'Duration'])
        df['Time'] = self.getNowTime()
        df['engine'] = '爱奇艺'
        df['Source'] = '爱奇艺'
        print df[:10]
        self.dfs.append((key, df))


        #df.to_csv('./data/youku_video_%s.csv' % key, encoding='utf-8', index=False)
        #df.to_excel('youku_video.xlsx', sheet_name= key, engine='xlsxwriter')

    def data_to_excel(self):
        with pd.ExcelWriter('./data/iqiyi_video.xlsx') as writer:
            for key, df in self.dfs:
                df.to_excel(writer, sheet_name=key)

    def getNowTime(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

class DataItem:
    def __init__(self):
        self.title = ''
        self.href = ''
        self.duration = ''

if __name__=='__main__':
    #key = raw_input('输入搜索关键字:')

    data = pd.read_excel('快乐阳光-监测片单.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
    print data.columns

    youkuVideo = IQiYiVideo()
    youkuVideo.run(data['key'].get_values())

    #key = '快乐大本营'
    #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))


