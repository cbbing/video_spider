# -*- coding: utf-8 -*-
#!/usr/bin/env python
#抓取acfun video搜索结果
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

class AcFunVideo(BaseVideo):
    def __init__(self):
        BaseVideo.__init__(self)
        self.engine = 'acfun'
        self.site = 'acfun'
        #self.album_url = 'http://so.v.163.com/search/000-0-0000-1-1-0-key/' #专辑的url
        self.general_url = 'http://www.acfun.tv/search/#query={key};page={pid}' #普通搜索的url
        self.filePath = 'acfun_video'

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

        start_time = GetNowTime()
        self.run_keys(keys)
        #self.run_keys_multithreading(keys)

        #重试运行三次
        # for _ in range(0, 3):
        #     self.run_unfinished_keys(keys, start_time)


    def search(self, key):

        items_all = []

        #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))

        url = self.general_url.format(key=key, pid=1)

        print 'start phantomjs', encode_wrap(url)

        driver = webdriver.Firefox()
        driver.get(url)

        driver.maximize_window()

        #普通
        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        lengthtypes = cf.get("acfun","lengthtype")
        lengthtypes = lengthtypes.strip('[').strip(']').split(',')
        for lengthtype in lengthtypes:

            try:
                # buttonText = self.timelengthDict[int(lengthtype)]
                #
                # # 模拟点击
                # driver.find_element_by_link_text(buttonText).click()


                # print encode_wrap('%s, 第一页,暂停%ds' % (buttonText, self.stop))
                # print '\n'
                # time.sleep(self.stop)

                #第一页
                items = self.parse_data(driver.page_source, 1, lengthtype, key)
                items_all.extend(items)

                #获取下一页
                try:
                    for i in range(self.pagecount-1):

                        url = self.general_url.format(key=key, pid=i+2)
                        driver.get(url)

                        time.sleep(self.stop)

                        items = self.parse_data(driver.page_source, i+2, lengthtype, key)
                        items_all.extend(items)

                except Exception,e:
                    print '未达到%d页，提前结束' % self.pagecount


            except Exception,e:
                print str(e)


        driver.quit()
        print 'parse phantomjs success '
        print 'item len:',len(items_all)
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

        dramaList = soup.findAll('div', {'class':'item block'})
        for drama in dramaList:

            try:
                item = DataItem()

                area_a = drama.find('a', {'class':'title','data-title':re.compile('.+')})
                item.title = area_a['data-title']
                item.href = 'http://www.acfun.tv' + area_a['href']

                #self.infoLogger.logger.info(encode_wrap('标题:' + item.title ))
                #self.infoLogger.logger.info(encode_wrap('链接:' + item.href))

                # durationTag = area_a.find('span', attrs={'class':'maskTx'})
                # if durationTag:
                #     item.duration = durationTag.text.strip()

                item.page = page
                # try:
                #     item.durationType = self.timelengthDict[int(legth_type)]
                # except Exception,e:
                #     print encode_wrap('未找到对应的时长类型!')

                items.append(item)
            except Exception,e:
                print e

        return items

if __name__=='__main__':
    #key = raw_input('输入搜索关键字:')

    data = pd.read_excel('keys.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
    print data

    video = AcFunVideo()
    video.run(data['key'].get_values()[:100])

    #key = '快乐大本营'
    #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))


