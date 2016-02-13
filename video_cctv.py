# -*- coding: utf-8 -*-
#抓取CCTV搜索结果

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import time
import requests
import re
import pandas as pd
from pandas import Series, DataFrame
from bs4 import BeautifulSoup as bs
from selenium import webdriver

from video_base import *

class CCTVVideo(BaseVideo):
    def __init__(self):
        BaseVideo.__init__(self)
        self.engine = '央视网'
        self.site = 'cctv'
        self.album_url = 'http://search.cctv.com/search.php?qtext={key}&type=video' #专辑的url
        self.general_url = 'http://search.cctv.com/ifsearch.php?qtext={key}&type=video&page={pid}&datepid=1&vtime={tid}' #普通搜索的url
        self.filePath = 'cctv_video'

        self.timelengthDict = {0:'不限', 1:'5分钟以内', 2:'5-30分钟', 3:'30-60分钟', 4:'大于1小时'} #时长类型对应网页中的按钮文字

        #self.infoLogger = Logger(logname=dir_log+'info_cctv(' + GetNowDate()+ ').log', logger='I')
        #self.errorLogger = Logger(logname=dir_log+'error_cctv(' + GetNowDate()+ ').log', logger='E')

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

        # 专辑
        album_url = self.album_url.format(key=key)
        # r = self.get_requests(album_url)
        # r.encoding = 'utf8'
        driver = webdriver.Firefox()
        driver.get(album_url)

        items_album = self.parse_data_album(driver)
        items_all.extend(items_album)

        driver.quit()

        # 普通
        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        lengthtypes = cf.get(self.site,"lengthtype")
        lengthtypes = lengthtypes.strip('[').strip(']').split(',')

        page_count = self.pagecount
        for lengthtype in lengthtypes:

            i = 0
            while i <  page_count:
                url = self.general_url.format(key=key, pid=i+1, tid=(int)(lengthtype)-1)

                #r = requests.get(soku_url)
                r = self.get_requests(url)
                r.encoding = 'utf8'

                if i == 0:
                    soup = bs(r.text, 'lxml')
                    real_pagecount = min(self.pagecount, self._get_page_count(soup))
                    page_count = min(real_pagecount, self.pagecount)

                items = self.parse_data(r.text, i+1, lengthtype, key)

                if items:
                    items_all.extend(items)
                else:
                    break

                i += 1

        return items_all


    # 专辑
    def parse_data_album(self, driver):

        items = []

        def get_top_album(soup, playlist='playlist_img_div'):
            """
            获取第一行的专辑
            """
            try:

                pFindMore = soup.find('p', {'class':'tv_rec'})
                if pFindMore:
                    aFindMore = pFindMore.find('a')
                    if aFindMore:
                        href_pre = aFindMore['href']
                        href_pre = href_pre.replace('videoset', 'video')

                drama = soup.find('div', attrs={'class':playlist})
                if drama:

                    liAll = drama.find_all('li')
                    for li in liAll:

                        item = DataItem()

                        a_last = li.find_all('a')[-1]
                        if a_last:
                            item.title = a_last.get_text().strip()
                            onclick_str = a_last['onclick']
                            f = re.findall('\'(.*?)\'', onclick_str)
                            if len(f) > 2:
                                item.href = href_pre + '/' + f[1]

                        durationTag = drama.find('div', {'class':'p_info'})
                        if durationTag:
                            item.duration = durationTag.text.strip()

                        item.page = 1
                        item.durationType = '专辑'

                        items.append(item)
            except Exception, e:
                print str(e)


        def get_more_album_list(driver):
            """
            获取更多专辑
            """
            try:
                driver.find_element_by_link_text('展开>>').click()

                soup = bs(driver.page_source, 'html5lib')
                moreList = soup.find_all('ul', {'class':'list_tv mt22 clearfix'})
                for more in moreList:
                    liList = more.find_all('li')
                    for li in liList:
                        a = li.find_all('a', {'href':'###'})
                        if len(a):
                            driver.find_element_by_link_text(a[-1].get_text()).click()
                            soup = bs(driver.page_source, 'html5lib')
                            soup_sub = soup.find('div', {'class':'list_tv_sub'})
                            get_top_album(soup_sub, playlist='playlist_img_div2')
            except Exception, e:
                print str(e)


        soup = bs(driver.page_source, 'html5lib')
        get_top_album(soup)
        get_more_album_list(driver)
        return items

    # 普通
    def parse_data(self, text, page, legth_type, key):

        items = []

        soup = bs(text, 'html5lib')
        data1 = soup.find_all('ul', {'class':'list_rec mt10 clearfix'})
        data2 = soup.find_all('ul', {'class':'list_rec clearfix'})

        #视频链接-全部结果
        dramaList = []
        dramaList1 = [d for data in data1 for d in data.find_all('li')]
        dramaList2 = [d for data in data2 for d in data.find_all('li')]
        dramaList.extend(dramaList1)
        dramaList.extend(dramaList2)

        for drama in dramaList:
            try:
                item = DataItem()

                area_a = drama.find_all('a')
                item.title = area_a[-1].get_text()
                item.href = area_a[-1]['href']

                #self.infoLogger.logger.info(encode_wrap('标题:' + item.title ))
                #self.infoLogger.logger.info(encode_wrap('链接:' + item.href))

                durationTag = drama.find('span')
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


    def _get_page_count(self, soup):
        """
        获取总页码
        :param soup:
        :return page_count:
        """

        try:

            pagerUL = soup.find('div', {'class':'ifpage'})
            data_pages = pagerUL.find_all('a')
            page_count = 0
            for a in data_pages:
                cur_count = (int)(a.get_text())
                if cur_count > page_count:
                    page_count = cur_count

        except Exception,e:
            # 只有一页
            page_count = 1
        return page_count

if __name__=='__main__':
    #key = raw_input('输入搜索关键字:')

    data = pd.read_excel('keys.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
    print data

    video = CCTVVideo()
    video.run(data['key'].get_values()[:100])

    #key = '快乐大本营'
    #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))


