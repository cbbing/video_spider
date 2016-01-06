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
        self.album_url = 'http://search.pptv.com/s_video?kw={key}' #专辑的url
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


    def search(self, key):

        items_all = []

        # 专辑
        album_url = self.album_url.format(key=key)
        r = self.get_requests(album_url)
        items_album = self.parse_data_album(r.text)
        items_all.extend(items_album)

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
            soup = bs(text, 'lxml')

            # 专辑一
            dramaList = soup.findAll('div', attrs={'class':'scon cf'})
            for drama in dramaList:

                item = DataItem()

                a = drama.find('a')
                if a:
                    item.title = a['title']
                    item.href = a['href']

                    jishu = drama.find('ul', {'class':'dlist3 cf'})
                    if jishu:
                        hrefAll = jishu.find_all('a')
                        if len(hrefAll) >= 2:
                            item.title += ' 第' + hrefAll[0].get_text() + "-" + hrefAll[-1].get_text() + '集'


                item.page = 1
                item.durationType = '专辑'

                items.append(item)

            # 专辑二
            drama2 = soup.find('ul', attrs={'class':'dlist cf'})
            if drama2:
                more_a_list = drama2.find_all('a')
                for more_a in more_a_list:
                    item = DataItem()
                    item.title = more_a['title']
                    item.href = more_a['href']

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
                item.durationType = '不限'

                items.append(item)
            except Exception,e:
                print e

        return items

if __name__=='__main__':
    #key = raw_input('输入搜索关键字:')

    data = pd.read_excel('keys.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
    print data

    video = PPTVVideo()
    video.run(data['key'].get_values()[:100])

    #key = '快乐大本营'
    #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))


