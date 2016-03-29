# -*- coding: utf-8 -*-
#!/usr/bin/env python
#抓取163video搜索结果
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

class WeiboVideo(BaseVideo):
    def __init__(self):
        BaseVideo.__init__(self)
        self.engine = '新浪微博'
        self.site = '163'
        self.album_url = 'http://so.v.163.com/search/000-0-0000-1-1-0-key/' #专辑的url
        self.general_url = 'http://so.v.163.com/search/000-0-tid-1-pid-0-key/' #普通搜索的url
        self.filePath = 'v163_video'

        self.timelengthDict = {0:'全部', 1:'10分钟以下', 2:'10-30分钟', 3:'30-60分钟', 4:'60分钟以上'} #时长类型对应网页中的按钮文字

        #self.infoLogger = Logger(logname=dir_log+'info_56(' + GetNowDate()+ ').log', logger='I')
        #self.errorLogger = Logger(logname=dir_log+'error_56(' + GetNowDate()+ ').log', logger='E')

    @fn_timer_
    def run(self, keys):

        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        lengthtypes = cf.get(self.site, "lengthtype")
        if len(lengthtypes.strip('[').strip(']')) == 0:
            print encode_wrap('配置为不运行')
            return
        return
        start_time = GetNowTime()
        #self.run_keys(keys)
        self.run_keys_multithreading(keys)

        #重试运行三次
        # for _ in range(0, 3):
        #     self.run_unfinished_keys(keys, start_time)


    def search(self, key):

        items_all = []

        # 专辑
        album_url = self.album_url.replace('key',key)
        r = self.get_requests(album_url)
        self.parse_data_album(r.text)

        #self.infoLogger.logger.info(encode_wrap('暂停%ds' % self.stop))
        print '*'*20, '暂停10s', '*'*20
        print '\n'
        time.sleep(self.stop)


        # 普通
        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        lengthtypes = cf.get(self.site,"lengthtype")
        lengthtypes = lengthtypes.strip('[').strip(']').split(',')
        for lengthtype in lengthtypes:

            for i in range(self.pagecount):
                url = self.general_url.replace('tid', lengthtype).replace('pid', str(i+1)).replace('key',key)

                #r = requests.get(soku_url)
                r = self.get_requests(url)
                items = self.parse_data(r.text, i+1, lengthtype, key)

                if items:
                    items_all.extend(items)
                else:
                    break

        return items_all


    # 专辑
    def parse_data_album(self, text):

        items = []

        try:
            soup = bs(text, 'lxml')

            #视频链接-专辑

            dramaList = soup.findAll('h2')
            for drama in dramaList:

                a = drama.find('a', title=re.compile('.+'))

                item = DataItem()

                item.title = a['title']
                item.href = a['href']

                if item.title == '查看详情':
                    continue

                item.page = 1
                item.durationType = '专辑'

                items.append(item)
        except Exception, e:
            print str(e)

        return items

    # 普通
    def parse_data(self, text, page, legth_type, key):

        items = []

        soup = bs(text, 'lxml')

        #视频链接-全部结果
        # tableArea = soup.find('div', {'class':'ssList area'})
        # if not tableArea:
        #     return []

        dramaList = soup.findAll('h3')
        for drama in dramaList:

            try:
                item = DataItem()

                area_a = drama.find('a')
                item.title = area_a.text
                item.href = area_a['href']

                #self.infoLogger.logger.info(encode_wrap('标题:' + item.title ))
                #self.infoLogger.logger.info(encode_wrap('链接:' + item.href))

                durationTag = area_a.find('span', attrs={'class':'maskTx'})
                if durationTag:
                    item.duration = durationTag.text.strip()

                item.page = page
                try:
                    item.durationType = self.timelengthDict[int(legth_type)]
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

    video = WeiboVideo()
    video.run(data['key'].get_values()[:100])

    #key = '快乐大本营'
    #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))


