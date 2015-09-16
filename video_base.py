# -*- coding: utf-8 -*-
#!/usr/bin/env python
#抓取优酷搜索结果
import sys
import time
import requests
import ConfigParser
from pandas import Series, DataFrame

reload(sys)
sys.setdefaultencoding("utf-8")

from bs4 import BeautifulSoup as bs
import pandas as pd

class BaseVideo:
    def __init__(self):

        cf = ConfigParser.ConfigParser()
        cf.read("config.ini")

        self.dfs = []
        self.items = []
        self.pagecount = int(cf.get("general","page_count"))
        self.filePath = ''
        self.engine = ''


    def create_data(self, key):
        df = DataFrame({'Title':[item.title for item in self.items], 'Href':[item.href for item in self.items], 'Duration':[item.duration for item in self.items]}, columns=['Title', 'Href', 'Duration'])
        df['Time'] = self.getNowTime()
        df['Engine'] = self.engine

        #df['Title'] = df['Title'].apply(lambda x : str(x).replace('【', '[').replace('】',']').replace('《','<').replace('》','>')) #([u'【',u'】',u'《',u'》'],['[',']','<','>'])
        #df['Title'] = df['Title'].apply(lambda x : str(x).decode('gbk','ignore').encode('utf8'))
        print df[:10]
        print '去重前，总个数:', len(df)
        df = df.drop_duplicates(['Href'])
        print '去重后，总个数:', len(df)
        self.dfs.append((key, df))


    def filter_short_video(self):
        items_temp = []
        for item in self.items:
            if len(str(item.duration)) > 0:

                mustFilter = True
                splits = str(item.duration).split(':')
                if len(splits) == 2:
                    minute = int(splits[0])
                    if minute >= 10:
                        mustFilter = False
                elif len(splits) == 3:
                    mustFilter = False

                if not mustFilter:
                    items_temp.append(item)
            else:
                items_temp.append(item)

        self.items = items_temp

    def data_to_excel(self):

        with pd.ExcelWriter(self.filePath) as writer:
            for key, df in self.dfs:
                df.to_excel(writer, sheet_name=key)
                #df.to_csv("./data/letv_video.csv")
                #break

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

    youkuVideo = BaseVideo()
    youkuVideo.run(data['key'].get_values())

    #key = '快乐大本营'
    #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))


