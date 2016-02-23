# -*- coding: utf-8 -*-
#!/usr/bin/env python
#抓取响巢看看视频搜索结果
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


class KankanVideo(BaseVideo):
    def __init__(self):
        BaseVideo.__init__(self)
        self.engine = '响巢看看'
        self.site = 'kankan'
        self.general_url = 'http://search.kankan.com/search.php?keyword=keys' #普通搜索的url
        self.filePath = 'kankan_video'

        self.timelengthDict = {0:'全部', 1:'10分钟以下', 2:'10-30分钟', 3:'30-60分钟', 4:'60分钟以上'} #时长类型对应网页中的按钮文字

        #self.infoLogger = Logger(logname=dir_log+'info_kankan(' + GetNowDate()+ ').log', logger='I')
        #self.errorLogger = Logger(logname=dir_log+'error_kankan(' + GetNowDate()+ ').log', logger='E')

    @fn_timer_
    def run(self, keys):

        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        lengthtypes = cf.get("kankan","lengthtype")
        if len(lengthtypes.strip('[').strip(']')) == 0:
            print encode_wrap('配置为不运行')
            return

        self.run_keys(keys)

        # for key in keys:
        #     try:
        #         # 初始化
        #         self.items = []
        #
        #         #搜索
        #         self.search(key)
        #
        #         #创建dataframe
        #         df = self.create_data(key)
        #
        #         self.data_to_sql_by_key(key, df)
        #
        #         print '\n'
        #         self.infoLogger.logger.info(encode_wrap('暂停%ds' % self.stop))
        #         print '\n'
        #         time.sleep(self.stop)
        #     except Exception,e:
        #         self.errorLogger.logger.info(key+'_unfinish_' + str(e))
        #         self.data_to_unfinish_file(self.web, key)
        #
        #
        # #保存数据
        # self.save_data()

    def search(self, key):

        items_all = []

        fun_url = self.general_url
        fun_url = fun_url.replace('keys',key)

        #self.infoLogger.logger.info(encode_wrap('start phantomjs'))
        #self.infoLogger.logger.info(encode_wrap(fun_url))

        #driver = webdriver.PhantomJS()
        driver = webdriver.Chrome()
        driver.get(fun_url)

        driver.get_screenshot_as_file("show.png")

        f = open('./data/data.html','w')
        f.write(driver.page_source)
        f.close()

        #专辑
        items = self.parse_data_album(driver.page_source, key)
        items_all.extend(items)

        # 模拟点击
        driver.find_element_by_link_text('筛选').click()

        #普通

        #普通
        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        lengthtypes = cf.get("kankan","lengthtype")
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
                items = self.parse_data(driver.page_source, 1, lengthtype, key)
                items_all.extend(items)

                #获取下一页
                try:
                    for i in range(self.pagecount-1):
                        driver.find_element_by_link_text('下一页').click()

                        #self.infoLogger.logger.info('%s, 下一页:%d, 暂停%ds' % (buttonText,(i+2), self.stop))
                        print encode_wrap('%s, 下一页:%d, 暂停%ds' % (buttonText,(i+2), self.stop))
                        print '\n'
                        time.sleep(self.stop)

                        items = self.parse_data(driver.page_source, i+2, lengthtype, key)
                        items_all.extend(items)

                except Exception,e:
                    infoLogger.logger.info('未达到%d页，提前结束' % self.pagecount)


            except Exception,e:
                info = '{0}:{1} 解析失败, LengthType:{3},{4}'.format(self.site, key, lengthtype, str(e))
                errorLogger.logger.error(info)


        driver.quit()
        #self.infoLogger.logger.info(encode_wrap('parse phantomjs success '))

        return items_all#

    # 专辑搜索
    def parse_data_album(self, text, key):

        items = []

        try:
            soup = bs(text)

            albumList = soup.findAll('ul', attrs={'class':'diversity_list diversity_list_zylist'})
            for album in albumList:

                #视频链接-专辑(样式一，如偶像来了等综艺节目）
                titleAndLinkList = album.findAll('a')
                for titleAndLink in titleAndLinkList:

                    try:
                        item = DataItem()

                        item.title = titleAndLink['title']
                        item.href = titleAndLink['href']

                        #self.infoLogger.logger.info(encode_wrap('标题:%s' % item.title))
                        #self.infoLogger.logger.info(encode_wrap('链接:%s' % item.href))

                        item.page = 1
                        item.durationType = '专辑'

                        items.append(item)
                    except Exception,e:
                        errorLogger.logger.error( "%s: 专辑解析出错:%s" % (key, str(e)))

        except Exception, e:
            print str(e)

        return items


    # 普通搜索
    def parse_data(self, text, page, lengthType, key):

        items = []

        try:

            soup = bs(text)

            source = soup.find("ul", attrs={'class':'imglist imglist_150x85'})
            if source:
                titleAndLinks = source.findAll('a')

                #视频链接
                for titleAndLink in titleAndLinks:

                    if titleAndLink:
                        try:
                            item = DataItem()

                            item.title = titleAndLink['title']
                            item.href = titleAndLink['href']

                            #self.infoLogger.logger.info(encode_wrap('标题:' + item.title))
                            #self.infoLogger.logger.info(encode_wrap('链接:' + item.href))

                            durationTag = titleAndLink.find('span', attrs={'class':'masktxt'})
                            if durationTag:
                                #self.infoLogger.logger.info(encode_wrap('时长:' + durationTag.text))
                                #print '时长:',durationTag.text
                                item.duration = durationTag.text

                            item.page = page
                            try:
                                item.durationType = self.timelengthDict[int(lengthType)]
                            except Exception,e:
                                print encode_wrap('未找到对应的时长类型!')

                            items.append(item)

                        except Exception,e:
                            errorLogger.logger.error(key + ":" + str(e))


        except Exception, e:
            errorLogger.logger.error(key + ":" + str(e))

        return items

if __name__=='__main__':
    #key = raw_input('输入搜索关键字:')

    data = pd.read_excel('keys.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
    print data

    video = KankanVideo()
    video.run(data['key'].get_values())

