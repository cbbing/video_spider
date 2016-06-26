# -*- coding: utf-8 -*-
#!/usr/bin/env python
# taobao搜索结果
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import pickle
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from video_base import *
from util.webHelper import get_web_driver

class Taobao(BaseVideo):

    dir_temp = 'data/cookie/'

    def __init__(self):
        BaseVideo.__init__(self)
        self.engine = '淘宝'
        self.site = 'taobao'
        self.album_url = '' #专辑的url
        self.general_url = 'https://s.taobao.com/search?q={key}&s={page}' #普通搜索的url
        self.filePath = 'taobao'

        self.timelengthDict = {0:'全部', 1:'10分钟以下', 2:'10-30分钟', 3:'30-60分钟', 4:'60分钟以上'} #时长类型对应网页中的按钮文字

        #self.infoLogger = Logger(logname=dir_log+'info_56(' + GetNowDate()+ ').log', logger='I')
        #self.errorLogger = Logger(logname=dir_log+'error_56(' + GetNowDate()+ ').log', logger='E')
        self.driver = get_web_driver(has_proxy=False)

    def __del__(self):
        if self.driver:
            self.driver.close()

    @fn_timer_
    def run(self, keys):


        self.run_keys(keys)
        # self.run_keys_multithreading(keys)

        #重试运行三次
        # for _ in range(0, 3):
        #     self.run_unfinished_keys(keys, start_time)


    def search(self, key):

        items_all = []

        # 普通

        driver = self.driver

        for page in range(0, self.pagecount):
            url = self.general_url.format(key=key, page = page*44)
            print url
            driver.get(url)

            items = self.parse_data(driver.page_source, page+1, key)

            if items:
                items_all.extend(items)
            else:
                break

        return items_all

    # 普通
    def parse_data(self, text, page, key):

        items = []

        soup = bs(text, 'lxml')

        #视频链接-全部结果
        # tableArea = soup.find('div', {'class':'ssList area'})
        # if not tableArea:
        #     return []

        dramaList = soup.find_all('div', {'class': "row row-2 title"})
        for drama in dramaList:

            try:
                item = DataItem()

                area_a = drama.find('a')
                if not area_a:
                    continue

                item.title = area_a.text.strip()

                href = area_a['href']
                print href
                if href.startswith('//'):
                    href = 'https:'+href
                item.href = href

                #self.infoLogger.logger.info(encode_wrap('标题:' + item.title ))
                #self.infoLogger.logger.info(encode_wrap('链接:' + item.href))

                item.page = page

                items.append(item)
            except Exception,e:
                print e

        return items

if __name__=='__main__':
    #key = raw_input('输入搜索关键字:')

    data = pd.read_excel('keys.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
    print data

    video = Taobao()
    print ','.join(data['key'].get_values()[:10])
    video.run(data['key'].get_values()[:10])

    #key = '快乐大本营'
    #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))


