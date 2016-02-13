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
from retrying import retry
from util.helper import fn_timer as fn_timer_

reload(sys)
sys.setdefaultencoding("utf-8")




class SokuVideo(BaseVideo):
    def __init__(self):
        BaseVideo.__init__(self)
        self.engine = '搜酷'
        self.album_url = '' #专辑的url
        self.general_url = '' #普通搜索的url

        self.timelengthDict = {0:'不限', 1:'0-10分钟', 2:'10-30分钟', 3:'30-60分钟', 4:'60分钟以上'} #时长类型对应网页中的按钮文字
        self.site = '' # youku or tudou

        #self.infoLogger = Logger(logname=dir_log + 'info_soku(' + GetNowDate()+ ').log', logger='I')
        #self.errorLogger = Logger(logname=dir_log+ 'error_soku(' + GetNowDate()+ ').log', logger='E')

    @fn_timer_
    def run(self, keys):

        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        lengthtypes = cf.get(self.site,"lengthtype")
        if len(lengthtypes.strip('[').strip(']')) == 0:
            print encode_wrap('配置为不运行')
            return

        start_time = GetNowTime()
        self.run_keys_multithreading(keys)

        #重试运行三次
        # for _ in range(0, 3):
        #     self.run_unfinished_keys(keys, start_time)



    def search(self, key):

        items_all = []

        # 专辑
        album_url = self.album_url.replace('key',key)
        #r = requests.get(album_url)
        r = self.get_requests(album_url)
        items = self.parse_data_album(r.text, key)
        items_all.extend(items)

        # self.infoLogger.logger.info(encode_wrap('暂停%ds' % self.stop))
        # #print '*'*20, '暂停10s'.decode('utf8'), '*'*20
        # print '\n'
        # time.sleep(self.stop)

        # 普通
        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        lengthtypes = cf.get(self.site,"lengthtype")
        lengthtypes = lengthtypes.strip('[').strip(']').split(',')
        for lengthtype in lengthtypes:

            for i in range(self.pagecount):
                soku_url = self.general_url.replace('tid', lengthtype)
                soku_url = soku_url.replace('pid', str(i+1))
                soku_url = soku_url.replace('key',key)

                #r = requests.get(soku_url)
                r = self.get_requests(soku_url)
                items = self.parse_data(r.text, i+1, lengthtype, key)

                if items:
                    items_all.extend(items)
                else:
                    break

                #self.infoLogger.logger.info(encode_wrap('暂停%ds, key:%s, Page %d, 时长Type:%s' % (self.stop, key, i+1, lengthtype)))
                #print '*'*20, '暂停10s, key:%s, Page %d, 时长Type:%s'.decode('utf8') % (key, i+1, lengthtype), '*'*20
                #print '\n'
                #time.sleep(self.stop)

        return items_all

    # 获取实际页数
    def get_real_page_count(self, html):
        soup = bs(html)
        sk_pager = soup.find('div', {'class':'sk_pager'})

        page_count = 1

        if sk_pager:
            pages = sk_pager.find_all('li')
            for page in pages:
                s = page.get_text()
                if s.isdigit() and int(s) > page_count:
                    page_count = int(s)

        return page_count

    # 专辑
    def parse_data_album(self, text, key):

        items = []

        soup = bs(text, 'html5lib')

        #视频链接-专辑
        #dramaList = soup.findAll('a', href=re.compile("^http://www.youku.com/playlist_show/"), title=re.compile(".+"))
        dramaList = soup.findAll('a', href=re.compile("^http://www.youku.com/playlist_show/|http://www.tudou.com/playlist/id/"), title=re.compile(".+"))
        for drama in dramaList:


            item = DataItem()

            try:


                # 2015-09-16， 搜库专辑链接变动了！
                # m = re.search(r"url=(.*?)&", drama['href'])
                # href = m.group(1)

                # 2016-02-02
                item.title = drama['title']
                item.href = drama['href']
                item.page = 1
                item.durationType = '专辑'

                #self.infoLogger.logger.info(encode_wrap('标题:%s' % drama['title']))
                #self.infoLogger.logger.info(encode_wrap('链接:%s' % href))
                # print '标题:'.decode('utf8'),drama['title'].decode('utf8')
                # print '链接:'.decode('utf8'),href
                items.append(item)

            except Exception, e:
                #print str(e)
                info = '{0}:{1}:{2}:{3}'.format(self.site, key, '专辑',str(e))
                self.errorLogger.logger.error(encode_wrap(info))

        return items


    # 普通
    def parse_data(self, text, page, lengthType, key):

        items = []

        soup = bs(text,'html5lib')

        #视频链接
        dramaList = soup.findAll('div', attrs={'class':'v-link'})
        for drama in dramaList:
            titleAndLink = drama.find('a')

            if titleAndLink:
                #self.infoLogger.logger.info(encode_wrap('Key:%s, Page:%d 标题:%s' % (key, page, titleAndLink['title'])))
                print encode_wrap('Key:%s, Page:%d 标题:%s' % (key, page, titleAndLink['title']))
                #self.infoLogger.logger.info(encode_wrap('链接:%s' % titleAndLink['href']))
                #print '标题:'.decode('utf8'),titleAndLink['title'].decode('gb18030')
                #print '链接:'.decode('utf8'),titleAndLink['href']

                item = DataItem()
                item.title = titleAndLink['title']
                item.href = titleAndLink['href']
                item.page = page
                try:
                    item.durationType = self.timelengthDict[int(lengthType)]
                except Exception,e:
                    print encode_wrap('未找到对应的时长类型!')

                items.append(item)
                # self.titles.append(titleAndLink['title'])
                # self.hrefs.append(titleAndLink['href'])

        # 视频时长
        dramaList_dura = soup.findAll('div', attrs={'class':'v-thumb'})
        for drama in dramaList_dura:
            titleAndImg = drama.findAll('img')

            if titleAndImg:
                #self.infoLogger.logger.info(encode_wrap('标题:%s' % titleAndImg[0]['alt']))
                print encode_wrap('标题:%s' % titleAndImg[0]['alt'])
                #print '标题:'.decode('utf8'),titleAndImg[0]['alt'].encode(sse, "replace").decode(sse)
                #print '图片链接:',titleAndImg[0]['src']

                for item in items:
                    if item.title == titleAndImg[0]['alt']:
                        vTime = dramaList[0].findAll('div')
                        if len(vTime) > 3:
                            #self.infoLogger.logger.info(encode_wrap('时长:%s' % vTime[3].text))
                            #print '时长:'.decode('utf8'),vTime[3].text
                            item.duration = vTime[3].text
                            break

        return items


def retry_if_result_none(result):
    return result is None

@retry(retry_on_result=retry_if_result_none)
def get_result():
    return None

if __name__=='__main__':

    data = pd.read_excel('keys.xlsx', '优酷网', index_col=None, na_values=['NA'])
    #print data.columns

    youkuVideo = SokuVideo()
    #youkuVideo.get_requests_data('http://www.baidu.com')
    youkuVideo.run_keys_multithreading(data['key'].get_values())
    #youkuVideo.run(['明若晓溪','旋风少女','偶像来了'])
    #key = '快乐大本营'
    #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))

    #print do_something_unreliable()
    #get_result()


