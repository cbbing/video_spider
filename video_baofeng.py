# -*- coding: utf-8 -*-
#!/usr/bin/env python
#抓取暴风影音视频搜索结果
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import time
import urllib
from bs4 import BeautifulSoup as bs
import pandas as pd
import ConfigParser
from pandas import Series, DataFrame
from selenium import webdriver
from video_base import *
from selenium.webdriver.support.ui import WebDriverWait


class BaofengVideo(BaseVideo):
    def __init__(self):
        BaseVideo.__init__(self)
        self.engine = '暴风影音'
        self.site = 'baofeng'
        self.general_url = 'http://www.baofeng.com/q{_page}_{_key}' #普通搜索的url
        self.filePath = 'baofeng_video'

        #self.timelengthDict = {0:'全部', 1:'10分钟以下', 2:'10-30分钟', 3:'30-60分钟', 4:'60分钟以上'} #时长类型对应网页中的按钮文字

        #self.infoLogger = Logger(logname=dir_log+'info_baofeng(' + GetNowDate()+ ').log', logger='I')
        #self.errorLogger = Logger(logname=dir_log+'error_baofeng(' + GetNowDate()+ ').log', logger='E')


    @fn_timer_
    def run(self, keys):

        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        lengthtypes = cf.get("baofeng","lengthtype")
        if len(lengthtypes.strip('[').strip(']')) == 0:
            print encode_wrap('配置为不运行')
            return

        self.run_keys(keys)


    def search(self, key):

        items_all = []

        fun_url = self.general_url.format(_page='', _key=key)
        r = self.get_requests(fun_url)
        r.encoding = 'utf8'

        #普通
        #第一页
        items = self.parse_data(r.text, 1, 0, key)  #暴风不支持时长选择，默认为0
        items_all.extend(items)

        #获取下一页
        try:
            for i in range(2, self.pagecount+1):

                print '\n'
                #self.infoLogger.logger.info(encode_wrap('下一页:%d, 暂停%ds' % ((i+2), self.stop)))
                print encode_wrap('下一页:%d, 暂停%ds' % ((i+2), self.stop))
                print '\n'
                time.sleep(self.stop)

                fun_url = self.general_url.format(_page=i, _key=key)
                r = self.get_requests(fun_url)
                r.encoding = 'utf8'

                items = self.parse_data(r.text, i, 0, key)
                items_all.extend(items)

        except Exception,e:
            self.infoLogger.logger.info(encode_wrap('未达到%d页，提前结束' % i))


        return items_all

    # 普通搜索
    def parse_data(self, text, page, lengthType, key):

        items = []

        try:

            soup = bs(text, 'lxml')

            titleAndLinks = soup.find_all('a', href=re.compile('^/detail/\d+/detail-\d+'), title=re.compile('.+'))
            for titleAndLink in titleAndLinks:

                item = DataItem()

                item.title = titleAndLink['title']
                item.href = titleAndLink['href']

                if not 'baofeng' in item.href:
                    item.href = 'http://www.baofeng.com' + item.href

                #self.infoLogger.logger.info(encode_wrap('标题:' + item.title + '  链接:' + item.href))

                # durationTag = titleAndLink.find('span', attrs={'class':'search-video-time'})
                # if durationTag:
                #     self.infoLogger.logger.info(encode_wrap('时长:' + durationTag.text))
                #     #print '时长:',durationTag.text
                #     item.duration = durationTag.text

                item.page = page
                try:
                    item.durationType = self.timelengthDict[int(lengthType)]
                except Exception,e:
                    print encode_wrap('未找到对应的时长类型!')

                items.append(item)


        except Exception, e:
            info = '{0}:{1} 解析失败, Page:{2}, LengthType:{3},{4}'.format(self.site, key, page, lengthType, str(e))
            self.errorLogger.logger.error(encode_wrap(str(e)))
            print str(e)

        return items

if __name__=='__main__':
    #key = raw_input('输入搜索关键字:')

    data = pd.read_excel('keys.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
    print data

    video = BaofengVideo()
    video.run(data['key'].get_values())

