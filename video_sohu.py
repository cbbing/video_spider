# -*- coding: utf-8 -*-
#!/usr/bin/env python
#抓取souhu搜索结果
import sys
import time
import requests
from pandas import Series, DataFrame

reload(sys)
sys.setdefaultencoding("utf-8")

from bs4 import BeautifulSoup as bs
import pandas as pd
from pandas import Series, DataFrame
from video_base import *
from util.codeConvert import *


class SouhuVideo(BaseVideo):
    def __init__(self):
        BaseVideo.__init__(self)
        self.engine = '搜狐'
        self.album_url = 'http://so.tv.sohu.com/mts?box=1&wd=key' #专辑的url
        self.general_url = 'http://so.tv.sohu.com/mts?wd=key&c=0&v=0&length=tid&limit=0&o=0&p=pid&st=' #普通搜索的url
        self.filePath = 'souhu_video'

        self.timelengthDict = {0:'不限', 1:'0-10分钟', 2:'10-30分钟', 3:'30-60分钟', 4:'60分钟以上'} #时长类型对应网页中的按钮文字

        self.infoLogger = Logger(logname='./data/log/info_sohu.log', logger='I')
        self.errorLogger = Logger(logname='./data/log/error_sohu.log', logger='E')

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


        #保存数据
        self.save_data()

    def search(self, key):

        # 专辑
        album_url = self.album_url.replace('key',key)
        r = requests.get(album_url)
        self.parse_data_album(r.text)

        self.infoLogger.logger.info(encode_wrap('暂停%ds' % self.stop))
        #print '*'*20, encode_wrap('暂停10s'), '*'*20
        print '\n'
        time.sleep(self.stop)

        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        lengthtypes = cf.get("sohu","lengthtype")
        lengthtypes = lengthtypes.strip('[').strip(']').split(',')
        for lengthtype in lengthtypes:

            for i in range(self.pagecount):
                url = self.general_url.replace('tid', lengthtype)
                url = url.replace('pid', str(i+1))
                url = url.replace('key',key)

                r = requests.get(url)
                self.parse_data(r.text, i+1, lengthtype)

                print '\n'
                self.infoLogger.logger.info(encode_wrap('暂停%ds, key:%s, Page %d, 时长Type:%s' % (self.stop, key, i+1, lengthtype)))
                #print '*'*20, encode_wrap('暂停10s, key:%s, Page %d, 时长Type:%s' % (key, i+1, lengthtype)), '*'*20
                print '\n'
                time.sleep(self.stop)


    # 专辑
    def parse_data_album(self, text):
        try:
            soup = bs(text)

            #视频链接-专辑
            dramaList = soup.findAll('div', attrs={'class':'seriesList'})
            for drama in dramaList:

                titleAndLinkList = drama.findAll('a')
                for titleAndLink in titleAndLinkList:

                    item = DataItem()

                    self.infoLogger.logger.info(encode_wrap('标题:%s' % titleAndLink['title']))
                    self.infoLogger.logger.info(encode_wrap('链接:%s' % titleAndLink['href']))
                    #print encode_wrap('标题:%s' % titleAndLink['title'])
                    #print encode_wrap('链接:%s' % titleAndLink['href'])
                    item.title = titleAndLink['title']
                    item.href = titleAndLink['href']
                    item.page = 1
                    item.durationType = '专辑'

                    self.items.append(item)
        except Exception, e:
            self.errorLogger.logger.error(encode_wrap(str(e)))
            print str(e)


    # 普通
    def parse_data(self, text, page, lengthType):
        soup = bs(text)

        #视频链接-全部结果
        dramaList = soup.findAll('div', attrs={'class':'pic170'})
        for drama in dramaList:

            item = DataItem()

            titleAndLink = drama.find('a')
            if titleAndLink:
                self.infoLogger.logger.info(encode_wrap('标题:%s' % titleAndLink['title']))
                self.infoLogger.logger.info(encode_wrap('链接:%s' % titleAndLink['href']))
                # print '标题:',titleAndLink['title']
                # print '链接:',titleAndLink['href']
                item.title = titleAndLink['title']
                item.href = titleAndLink['href']

                durationTag = drama.find('span', attrs={'class':'maskTx'})
                if durationTag:
                    item.duration = durationTag.text

                item.page = page
                try:
                    item.durationType = self.timelengthDict[int(lengthType)]
                except Exception,e:
                    self.errorLogger.logger.error(encode_wrap('未找到对应的时长类型!'))


            self.items.append(item)



if __name__=='__main__':
    #key = raw_input('输入搜索关键字:')

    data = pd.read_excel('keys.xlsx', 'Sheet2', index_col=None, na_values=['NA'])
    print data

    youkuVideo = SouhuVideo()
    youkuVideo.run(data['key'].get_values())

    #key = '快乐大本营'
    #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))


