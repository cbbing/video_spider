# -*- coding: utf-8 -*-
#!/usr/bin/env python
#抓取腾讯视频搜索结果
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


class QQVideo(BaseVideo):
    def __init__(self):
        BaseVideo.__init__(self)
        self.engine = '腾讯'
        self.site = 'qq'
        self.general_url = 'http://v.qq.com/search.html?pagetype=3&stj2=search.search&stag=txt.index&ms_key=keys' #普通搜索的url
        self.filePath = 'qq_video'

        self.timelengthDict = {0:'全部', 1:'10分钟以下', 2:'10-30分钟', 3:'30-60分钟', 4:'60分钟以上'} #时长类型对应网页中的按钮文字

        #self.infoLogger = Logger(logname=dir_log+'info_qq(' + GetNowDate()+ ').log', logger='I')
        #self.errorLogger = Logger(logname=dir_log+'error_qq(' + GetNowDate()+ ').log', logger='E')


    @fn_timer_
    def run(self, keys):

        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        lengthtypes = cf.get("qq","lengthtype")
        if len(lengthtypes.strip('[').strip(']')) == 0:
            print encode_wrap('配置为不运行')
            return

        self.run_keys(keys)


    def search(self, key):

        items_all = []

        #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))

        qq_url = self.general_url
        qq_url = qq_url.replace('keys',key)

        #self.infoLogger.logger.info(encode_wrap('start phantomjs'))
        #self.infoLogger.logger.info(encode_wrap(qq_url))

        #driver = webdriver.PhantomJS()
        driver = webdriver.Firefox()
        driver.get(qq_url)

        #专辑
        items = self.parse_data_album(driver)
        items_all.extend(items)

        #模拟点击"V",让时长按钮可见
        element = driver.find_element_by_xpath('//a[@class="btn_arrow _cox_filter_btn"]')
        element.click()

        #普通
        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        lengthtypes = cf.get("qq","lengthtype")
        lengthtypes = lengthtypes.strip('[').strip(']').split(',')
        for lengthtype in lengthtypes:

            try:
                buttonText = self.timelengthDict[int(lengthtype)]
                # 模拟点击
                driver.find_element_by_link_text(buttonText).click()

                #self.infoLogger.logger.info(encode_wrap('%s, 第一页,暂停%ds' % (buttonText, self.stop)))
                print encode_wrap('%s, 第一页,暂停%ds' % (buttonText, self.stop))
                print '\n'
                time.sleep(self.stop)

                #第一页
                items = self.parse_data(driver.page_source, 1, lengthtype)
                items_all.extend(items)

                #获取下一页
                try:
                    for i in range(self.pagecount-1):
                        driver.find_element_by_link_text('下一页').click()

                        #self.infoLogger.logger.info(encode_wrap('%s, 下一页:%d, 暂停%ds' % (buttonText,(i+2), self.stop)))
                        print encode_wrap('%s, 下一页:%d, 暂停%ds' % (buttonText,(i+2), self.stop))
                        print '\n'
                        time.sleep(self.stop)

                        items = self.parse_data(driver.page_source, i+2, lengthtype)
                        items_all.extend(items)

                except Exception,e:
                    self.infoLogger.logger.info(encode_wrap('未达到%d页，提前结束' % i))


            except Exception,e:
                self.errorLogger.logger.error(encode_wrap(str(e)))


        driver.quit()
        #self.infoLogger.logger.info(encode_wrap('parse phantomjs success '))

        return items_all

    # 专辑搜索
    def parse_data_album(self, driver):

        items = []

        # def get_album1():
        #     soup = bs(driver.page_source, 'lxml')
        #     album = soup.find('div', {'class':'mod_search_detail search_detail_event cf'})
        #     if album:
        #         a = album.find('a')
        #         if a:
        #             item = DataItem()
        #             item.title = a['title']
        #             item.href = a['href']
        #             item.page = 1
        #             item.durationType = '专辑'
        #
        #             items.append(item)
        #
        # def get_album2():
        #
        #     soup = bs(driver.page_source, 'lxml')
        #
        #     liAll = soup.find_all('li', {'class':'list_item _albums_cont'})
        #     for li in liAll:
        #         h2 = li.find('h2', {'class':'result_title'})
        #         albumTitle =h2.get_text()
        #
        #         divAll = li.find_all('div', {'class':'mod_album_titlist_lists video_play_list_cont'})
        #         if not divAll:
        #             continue
        #         for div in divAll:
        #             aAll = div.find_all('a')
        #             for a in aAll:
        #
        #                 item = DataItem()
        #                 item.title = albumTitle + ' ' + a['title']
        #                 item.href = a['href']
        #                 item.page = 1
        #                 item.durationType = '专辑'
        #
        #                 items.append(item)
        #
        # def get_album3():
        #     """
        #     片花
        #     """
        #     soup = bs(driver.page_source, 'lxml')
        #
        #     liAll = soup.find_all('li', {'class':'list_item _albums_cont'})
        #     for li in liAll:
        #         h2 = li.find('h2', {'class':'result_title'})
        #         albumTitle =h2.get_text()
        #
        #         divAll = li.find_all('div', {'class':'mod_figures_preview'})
        #         for div in divAll:
        #             liAll = div.find_all('li')
        #             for li in liAll:
        #                 a = li.find('a')
        #                 if a:
        #                     item = DataItem()
        #                     item.title = '片花 ' + albumTitle + ' ' + a['title']
        #                     item.href = a['href']
        #                     item.page = 1
        #                     item.durationType = '专辑'
        #
        #                     items.append(item)
        #
        #
        # def click_year_lab():
        #     """
        #     模拟点击年份标签, 让JS渲染出各个年份的专辑链接地址
        #     """
        #
        #     yearLabs = []
        #
        #     soup = bs(driver.page_source, 'lxml')
        #     multilineAll = soup.find_all('div', {'class':'mod_album_titlist_title mod_album_titlist_title_multiline'})
        #     for multiline in multilineAll:
        #         aAll = multiline.find_all('a')
        #         for a in aAll:
        #             yearLabs.append(a.get_text())
        #
        #     for lab in set(yearLabs):
        #         try:
        #             btn_years = driver.find_elements_by_link_text(lab)
        #             for btn in btn_years:
        #                 btn.click()
        #         except:
        #             None


        try:
            # click_year_lab()
            # get_album1()
            # get_album2()
            # get_album3()

            soup = bs(driver.page_source, 'html5lib')
            dramaList = soup.findAll('a', href=re.compile("^http://m.v.qq.com/pgm/|/detail/\d+/"), title=re.compile(".+"))
            for drama in dramaList:
                item = DataItem()
                item.title = drama['title']
                item.href = drama['href']
                item.page = 1
                item.durationType = '专辑'

                items.append(item)


        except Exception,e:
            self.errorLogger.logger.error(encode_wrap( "专辑解析出错:%s" % str(e)))


        return items

    # 普通搜索
    def parse_data(self, text, page, lengthType):

        items = []

        try:

            soup = bs(text, 'lxml')

            source = soup.find("ul", attrs={'class':'mod_figure_list mod_figure_list_190'})
            if source:
                titleAndLinks = source.findAll('a')

                #视频链接
                for titleAndLink in titleAndLinks:
                    try:

                        if titleAndLink:

                            item = DataItem()

                            #self.infoLogger.logger.info(encode_wrap('标题:' + titleAndLink['title']))
                            #self.infoLogger.logger.info(encode_wrap('链接:' + titleAndLink['href']))
                            # print '标题:',titleAndLink['title']
                            # print '链接:',titleAndLink['href']
                            item.title = titleAndLink['title']
                            item.href = titleAndLink['href']

                            durationTag = titleAndLink.find('span', attrs={'class':'new_info'})
                            if durationTag:
                                #self.infoLogger.logger.info(encode_wrap('时长:' + durationTag.text))
                                #print '时长:',durationTag.text
                                item.duration = durationTag.text

                            item.page = page
                            try:
                                item.durationType = self.timelengthDict[int(lengthType)]
                            except Exception,e:
                                self.errorLogger.logger.error(encode_wrap('未找到对应的时长类型!'))

                            items.append(item)

                    except Exception,e:
                        self.errorLogger.logger.error(encode_wrap(str(e)))
                        #print str(e)

        except Exception, e:
            self.errorLogger.logger.error(encode_wrap(str(e)))

        return items

if __name__=='__main__':
    #key = raw_input('输入搜索关键字:')

    data = pd.read_excel('keys.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
    print data

    video = QQVideo()
    video.run(data['key'].get_values())

