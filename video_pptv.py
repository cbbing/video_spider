# -*- coding: utf-8 -*-
#!/usr/bin/env python
#抓取PPTV搜索结果
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

class PPTVVideo(BaseVideo):
    def __init__(self):
        BaseVideo.__init__(self)
        self.engine = 'PPTV'
        self.site = 'pptv'
        self.album_url = 'http://so.pptv.com/so/q_key' #专辑的url
        self.general_url = 'http://search.pptv.com/result?search_query=key&p=pid' #普通搜索的url
        self.filePath = 'pptv_video'

        self.timelengthDict = {0:'全部', 2:'10分钟以下', 3:'10-30分钟', 4:'30-60分钟', 5:'60分钟以上'} #时长类型对应网页中的按钮文字

        self.infoLogger = Logger(logname=dir_log+'info_pptv(' + GetNowDate()+ ').log', logger='I')
        self.errorLogger = Logger(logname=dir_log+'error_pptv(' + GetNowDate()+ ').log', logger='E')

    @fn_timer_
    def run(self, keys):

        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        lengthtypes = cf.get("pptv","lengthtype")
        if len(lengthtypes.strip('[').strip(']')) == 0:
            print encode_wrap('配置为不运行')
            return

        start_time = GetNowTime()
        #self.run_keys(keys)
        self.run_keys_multithreading(keys)

        # #重试运行三次
        # for _ in range(0, 3):
        #     self.run_unfinished_keys(keys, start_time)


    def search(self, key):

        items_all = []

        # 专辑
        #album_url = self.album_url.replace('key',key)
        #r = requests.get(album_url)
        #r = self.get_requests(album_url)
        #self.parse_data_album(r.text)

        #self.infoLogger.logger.info(encode_wrap('暂停%ds' % self.stop))
        #print '*'*20, '暂停10s', '*'*20
        #print '\n'
        #time.sleep(self.stop)


        # 普通
        for i in range(self.pagecount):
            url = self.general_url
            url = url.replace('pid', str(i+1))
            url = url.replace('key',key)

            #r = requests.get(url)
            r = self.get_requests(url)
            items = self.parse_data(r.text, i+1, key)
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
    def parse_data(self, text, page, key):

        items = []

        soup = bs(text)

        #视频链接-全部结果
        dramaList = soup.findAll('a', attrs={'class':'ui-list-ct'})
        for drama in dramaList:

            try:
                item = DataItem()

                item.title = drama['title']
                item.href = drama['href']

                self.infoLogger.logger.info(encode_wrap('标题:' + item.title ))
                #self.infoLogger.logger.info(encode_wrap('链接:' + item.href))

                durationTag = drama.find('p', attrs={'class':'ui-pic'})
                if durationTag:
                    item.duration = durationTag.text.strip()

                item.page = page

                items.append(item)
            except Exception,e:
                print e

        return items

if __name__=='__main__':
    #key = raw_input('输入搜索关键字:')

    data = pd.read_excel('keys.xlsx', 'pptv', index_col=None, na_values=['NA'])
    print data

    video = PPTVVideo()
    video.run(data['key'].get_values()[:100])

    #key = '快乐大本营'
    #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))


