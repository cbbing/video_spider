# -*- coding: utf-8 -*-
#!/usr/bin/env python
#抓取优酷搜索结果
import sys
import time
import re
import ConfigParser
from pandas import Series, DataFrame

reload(sys)
sys.setdefaultencoding("utf-8")

from bs4 import BeautifulSoup as bs
import pandas as pd
from util.MyLogger import InfoLogger, ErrorLogger

class BaseVideo:
    def __init__(self):

        cf = ConfigParser.ConfigParser()
        cf.read("config.ini")

        self.dfs = []
        self.items = []
        self.pagecount = int(cf.get("general","page_count"))
        self.filePath = ''
        self.engine = ''

        self.stop = 3 # 暂停3s


    def create_data(self, key):
        df = DataFrame({'Title':[item.title for item in self.items],
                        'Href':[item.href for item in self.items],
                        'Duration':[item.duration for item in self.items],
                        'Page':[item.page for item in self.items],
                        'DurationType':[item.durationType for item in self.items]
                        },
                       columns=['Title', 'Href', 'Duration', 'DurationType', 'Page'])
        print df[:10]
        df['Time'] = self.getNowTime()
        df['Engine'] = self.engine
        df['Source'] = df['Href'].apply(lambda x : self.get_video_source(x))

        # if df['Duration'].any() == '':
        #     df = df.drop('Duration', axis=1)

        #df['Title'] = df['Title'].apply(lambda x : str(x).replace('【', '[').replace('】',']').replace('《','<').replace('》','>')) #([u'【',u'】',u'《',u'》'],['[',']','<','>'])
        #df['Title'] = df['Title'].apply(lambda x : str(x).decode('gbk','ignore').encode('utf8'))
        print df[:10]

        InfoLogger.addLog('去重前，总个数:%d' % len(df))
        df = df.drop_duplicates(['Href'])
        InfoLogger.addLog('去重后，总个数:%d' % len(df))
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
        InfoLogger.addLog('写入excel完成')

    def getNowTime(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

    # 判断视频来源
    def get_video_source(self, url):
        dictSource = {'hunantv':'芒果TV', 'youku':'优酷', 'tudou':'土豆',
                      'iqiyi':'爱奇艺','letv':'乐视','sina':'新浪视频',
                      'sohu':'搜狐视频', 'qq':'腾讯视频','wasu':'华数',
                      'ifeng':'凤凰视频', '56':'56', '1905':'1905电影网',
                      'kankan':'响巢看看', 'cntv':'CNTV','ku6':'酷6'}

        try:
            m = re.search(r"\.(\w*?)\.[com|cn]", url)  #\w匹配[a-zA-z0-9]
            key = m.group(1) #如hunantv
            return dictSource[key]
        except Exception, e:
            ErrorLogger.addLog(str(e))
            return ''


class DataItem:
    def __init__(self):
        self.title = ''
        self.href = ''
        self.duration = ''
        self.page = 0 #页码
        self.durationType = '' #时长类型

if __name__=='__main__':
    #key = raw_input('输入搜索关键字:')

    data = pd.read_excel('keys.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
    print data.columns

    youkuVideo = BaseVideo()
    youkuVideo.run(data['key'].get_values())

    #key = '快乐大本营'
    #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))


