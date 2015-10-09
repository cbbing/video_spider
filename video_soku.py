# -*- coding: utf-8 -*-
#!/usr/bin/env python
#抓取优酷搜索结果
import sys
import time
import requests
import ConfigParser
import re
from video_base import *
from bs4 import BeautifulSoup as bs
import pandas as pd
from util.MyLogger import InfoLogger, ErrorLogger

reload(sys)
sys.setdefaultencoding("utf-8")




class SokuVideo(BaseVideo):
    def __init__(self):
        BaseVideo.__init__(self)
        self.engine = '搜酷'
        self.album_url = '' #专辑的url
        self.general_url = '' #普通搜索的url

        self.timelengthDict = {0:'不限', 1:'0-10分钟', 2:'10-30分钟', 3:'30-60分钟', 4:'60分钟以上'} #时长类型对应网页中的按钮文字
        self.web = '' # youku or tudou

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

            print '\n'*2
            #print '*'*20, '暂停10s'.decode('utf8'), '*'*20
            self.infoLogger.logger.info(encode_wrap('暂停%ds' % self.stop))
            print '\n'*2
            time.sleep(self.stop)



        #存入excel
        self.data_to_excel()

    def search(self, key):

        # 专辑
        album_url = self.album_url.replace('key',key)
        r = requests.get(album_url)
        self.parse_data_album(r.text)

        self.infoLogger.logger.info(encode_wrap('暂停%ds' % self.stop))
        #print '*'*20, '暂停10s'.decode('utf8'), '*'*20
        print '\n'
        time.sleep(self.stop)

        # 普通
        cf = ConfigParser.ConfigParser()
        cf.read("config.ini")
        lengthtypes = cf.get(self.web,"lengthtype")
        lengthtypes = lengthtypes.strip('[').strip(']').split(',')
        for lengthtype in lengthtypes:

            for i in range(self.pagecount):
                soku_url = self.general_url.replace('tid', lengthtype)
                soku_url = soku_url.replace('pid', str(i+1))
                soku_url = soku_url.replace('key',key)

                r = requests.get(soku_url)
                self.parse_data(r.text, i+1, lengthtype)

                self.infoLogger.logger.info(encode_wrap('暂停%ds, key:%s, Page %d, 时长Type:%s' % (self.stop, key, i+1, lengthtype)))
                #print '*'*20, '暂停10s, key:%s, Page %d, 时长Type:%s'.decode('utf8') % (key, i+1, lengthtype), '*'*20
                print '\n'
                time.sleep(self.stop)


    # 专辑
    def parse_data_album(self, text):
        soup = bs(text)

        #视频链接-专辑
        dramaList = soup.findAll('a', attrs={'class':'accordion-toggle collapsed'})
        for drama in dramaList:

            item = DataItem()

            try:


                # 2015-09-16， 搜库专辑链接变动了！
                m = re.search(r"url=(.*?)&", drama['href'])
                href = m.group(1)

                item.title = drama['title']
                item.href = href
                item.page = 1
                item.durationType = '专辑'

                self.infoLogger.logger.info(encode_wrap('标题:%s' % drama['title']))
                self.infoLogger.logger.info(encode_wrap('链接:%s' % href))
                # print '标题:'.decode('utf8'),drama['title'].decode('utf8')
                # print '链接:'.decode('utf8'),href
                self.items.append(item)

            except Exception, e:
                #print str(e)
                self.errorLogger.logger.info(encode_wrap(str(e)))



    # 普通
    def parse_data(self, text, page, lengthType):
        soup = bs(text)

        sse = sys.stdout.encoding

        #视频链接
        dramaList = soup.findAll('div', attrs={'class':'v-link'})
        for drama in dramaList:
            titleAndLink = drama.find('a')

            if titleAndLink:
                self.infoLogger.logger.info(encode_wrap('标题:%s' % titleAndLink['title']))
                self.infoLogger.logger.info(encode_wrap('链接:%s' % titleAndLink['href']))
                #print '标题:'.decode('utf8'),titleAndLink['title'].decode('gb18030')
                #print '链接:'.decode('utf8'),titleAndLink['href']

                item = DataItem()
                item.title = titleAndLink['title']
                item.href = titleAndLink['href']
                item.page = page
                try:
                    item.durationType = self.timelengthDict[int(lengthType)]
                except Exception,e:
                    self.errorLogger.logger.info(encode_wrap('未找到对应的时长类型!'))

                self.items.append(item)
                # self.titles.append(titleAndLink['title'])
                # self.hrefs.append(titleAndLink['href'])

        # 视频时长
        dramaList = soup.findAll('div', attrs={'class':'v-thumb'})
        for drama in dramaList:
            titleAndImg = drama.findAll('img')

            if titleAndImg:
                self.infoLogger.logger.info(encode_wrap('标题:%s' % titleAndImg[0]['alt']))
                #print '标题:'.decode('utf8'),titleAndImg[0]['alt'].encode(sse, "replace").decode(sse)
                #print '图片链接:',titleAndImg[0]['src']

                for item in self.items:
                    if item.title == titleAndImg[0]['alt']:
                        vTime = dramaList[0].findAll('div')
                        if len(vTime) > 3:
                            self.infoLogger.logger.info(encode_wrap('时长:%s' % vTime[3].text))
                            #print '时长:'.decode('utf8'),vTime[3].text
                            item.duration = vTime[3].text
                            break


if __name__=='__main__':

    data = pd.read_excel('keys.xlsx', 'Sheet2', index_col=None, na_values=['NA'])
    print data.columns

    youkuVideo = SokuVideo()
    youkuVideo.run(data['key'].get_values())
    #youkuVideo.run(['明若晓溪','旋风少女','偶像来了'])
    #key = '快乐大本营'
    #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))


