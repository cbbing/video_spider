# -*- coding: utf-8 -*-
#!/usr/bin/env python
#抓取爱奇艺搜索结果
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

class IQiYiVideo(BaseVideo):
    def __init__(self):
        BaseVideo.__init__(self)
        self.engine = '爱奇艺'
        self.site = 'iqiyi'
        self.album_url = 'http://so.iqiyi.com/so/q_key' #专辑的url
        self.general_url = 'http://so.iqiyi.com/so/q_key_ctg__t_tid_page_pid_p_1_qc_0_rd__site_iqiyi_m_1_bitrate_' #普通搜索的url
        self.filePath = 'iqiyi_video'

        self.timelengthDict = {0:'全部', 2:'10分钟以下', 3:'10-30分钟', 4:'30-60分钟', 5:'60分钟以上'} #时长类型对应网页中的按钮文字

        self.infoLogger = Logger(logname=dir_log+'info_iqiyi(' + GetNowDate()+ ').log', logger='I')
        self.errorLogger = Logger(logname=dir_log+'error_iqiyi(' + GetNowDate()+ ').log', logger='E')


    def run(self, keys):

        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        lengthtypes = cf.get("iqiyi","lengthtype")
        if len(lengthtypes.strip('[').strip(']')) == 0:
            print encode_wrap('配置为不运行')
            return

        start_time = GetNowTime()
        self.run_keys_multithreading(keys)

        #重试运行三次
        for _ in range(0, 3):
            self.run_unfinished_keys(keys, start_time)


    def search(self, key):

        items_all = []

        # 专辑
        album_url = self.album_url.replace('key',key)
        #r = requests.get(album_url)
        r = self.get_requests(album_url)
        items = self.parse_data_album(r.text)
        items_all.extend(items)

        # 普通
        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        lengthtypes = cf.get("iqiyi","lengthtype")
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
            soup = bs(text)

            #视频链接-专辑
            dramaList = soup.findAll('a', attrs={'class':'album_link'})
            for drama in dramaList:

                item = DataItem()

                self.infoLogger.logger.info(encode_wrap('标题:' + drama['title']))
                self.infoLogger.logger.info(encode_wrap('链接:' + drama['href']))
                item.title = drama['title']
                item.href = drama['href']

                item.page = 1
                item.durationType = '专辑'

                items.append(item)
        except Exception, e:
                print str(e)

        return items

    # 普通
    def parse_data(self, text, page, lengthType):

        items = []

        soup = bs(text)

        #视频链接-全部结果
        dramaList = soup.findAll('a', attrs={'class':'figure  figure-180101 '})
        for drama in dramaList:

            try:
                item = DataItem()

                titleAndLink = drama.find('img')
                if titleAndLink:
                    self.infoLogger.logger.info(encode_wrap('标题:' + titleAndLink['title']))
                    self.infoLogger.logger.info(encode_wrap('链接:' + drama['href']))#titleAndLink['href']
                    item.title = titleAndLink['title']
                    item.href = drama['href']
                durationTag = drama.find('span', attrs={'class':'v_name'})
                if durationTag:
                    item.duration = durationTag.text

                item.page = page
                try:
                    item.durationType = self.timelengthDict[int(lengthType)]
                except Exception,e:
                    print encode_wrap('未找到对应的时长类型!')

                items.append(item)
            except Exception,e:
                print e

        return items

if __name__=='__main__':
    #key = raw_input('输入搜索关键字:')

    data = pd.read_excel('keys.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
    print data

    youkuVideo = IQiYiVideo()
    youkuVideo.run(data['key'].get_values())

    #key = '快乐大本营'
    #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))


