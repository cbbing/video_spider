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
from util.CodeConvert import *


class SouhuVideo(BaseVideo):
    def __init__(self):
        BaseVideo.__init__(self)
        self.engine = '搜狐'
        self.site = 'sohu'
        self.album_url = 'http://so.tv.sohu.com/mts?box=1&wd=key' #专辑的url
        self.general_url = 'http://so.tv.sohu.com/mts?wd=key&c=0&v=0&length=tid&limit=0&o=0&p=pid&st=' #普通搜索的url
        self.filePath = 'souhu_video'

        self.timelengthDict = {0:'不限', 1:'0-10分钟', 2:'10-30分钟', 3:'30-60分钟', 4:'60分钟以上'} #时长类型对应网页中的按钮文字

        self.infoLogger = Logger(logname=dir_log+'info_sohu(' + GetNowDate()+ ').log', logger='I')
        self.errorLogger = Logger(logname=dir_log+'error_sohu(' + GetNowDate()+ ').log', logger='E')

    @fn_timer_
    def run(self, keys):

        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        lengthtypes = cf.get("sohu","lengthtype")
        if len(lengthtypes.strip('[').strip(']')) == 0:
            print encode_wrap('配置为不运行')
            return

        start_time = GetNowTime()
        #self.run_keys(keys)
        self.run_keys_multithreading(keys)

        #重试运行三次
        #for _ in range(0, 3):
        #    self.run_unfinished_keys(keys, start_time)


    def search(self, key):

        items_all = []

        # 专辑
        album_url = self.album_url.replace('key',key)
        #r = requests.get(album_url)
        r = self.get_requests(album_url)
        items = self.parse_data_album(r.text)
        items_all.extend(items)

        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        lengthtypes = cf.get("sohu","lengthtype")
        lengthtypes = lengthtypes.strip('[').strip(']').split(',')
        for lengthtype in lengthtypes:

            for i in range(self.pagecount):
                url = self.general_url.replace('tid', lengthtype)
                url = url.replace('pid', str(i+1))
                url = url.replace('key',key)

                #r = requests.get(url)
                r = self.get_requests(url)
                items = self.parse_data(r.text, i+1, lengthtype)
                items_all.extend(items)

        return items_all

    # 专辑
    def parse_data_album(self, text):

        items = []

        try:
            soup = bs(text, 'lxml')

            #视频链接-专辑
            drama = soup.find('div', attrs={'class':'area  special'})
            if drama:

                divAll = drama.find_all('div', {'class':'infoA cfix'})
                for div in divAll:
                    a = div.find('a')

                    item = DataItem()

                    item.title = a['title']
                    item.href = a['href']
                    item.page = 1
                    item.durationType = '专辑'

                    items.append(item)
        except Exception, e:
            self.errorLogger.logger.error(encode_wrap(str(e)))


        return items


    # 普通
    def parse_data(self, text, page, lengthType):

        items = []

        soup = bs(text, 'lxml')

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


            items.append(item)

        return items


if __name__=='__main__':
    #key = raw_input('输入搜索关键字:')

    data = pd.read_excel('keys.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
    print data

    youkuVideo = SouhuVideo()
    youkuVideo.run(data['key'].get_values()[:100])

    #key = '快乐大本营'
    #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))


