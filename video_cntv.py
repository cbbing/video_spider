# -*- coding: utf-8 -*-
#!/usr/bin/env python
#抓取CNTV搜索结果
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


class CNTVVideo(BaseVideo):
    def __init__(self):
        BaseVideo.__init__(self)
        self.engine = '央视网'
        self.site = 'cctv'
        self.general_url = 'http://search.cctv.com/search.php?qtext={key}&type=video' #普通搜索的url
        self.filePath = 'cctv_video'

        self.timelengthDict = {0:'不限', 1:'5分钟以内', 2:'5-30分钟', 3:'30-60分钟', 4:'大于1小时'} #时长类型对应网页中的按钮文字

        self.infoLogger = Logger(logname=dir_log+'info_qq(' + GetNowDate()+ ').log', logger='I')
        self.errorLogger = Logger(logname=dir_log+'error_qq(' + GetNowDate()+ ').log', logger='E')


    @fn_timer_
    def run(self, keys):

        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        lengthtypes = cf.get("cctv","lengthtype")
        if len(lengthtypes.strip('[').strip(']')) == 0:
            print encode_wrap('配置为不运行')
            return

        self.run_keys(keys)


    def search(self, key):

        items_all = []

        #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))

        cntv_url = self.general_url.format(key=key)

        print 'start phantomjs', encode_wrap(cntv_url)

        #driver = webdriver.PhantomJS()
        driver = webdriver.Firefox()
        driver.get(cntv_url)

        driver.maximize_window()
        siz = driver.get_window_size()
        driver.set_window_size(siz['width'], siz['height']*2)

        driver.get_screenshot_as_file("show.png")

        f = open('./data/data.html','w')
        f.write(driver.page_source)
        f.close()

        #普通
        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        lengthtypes = cf.get("cctv","lengthtype")
        lengthtypes = lengthtypes.strip('[').strip(']').split(',')
        for lengthtype in lengthtypes:

            try:
                buttonText = self.timelengthDict[int(lengthtype)]
                # 模拟点击
                #driver.find_element_by_link_text(buttonText).click()

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

                        self.infoLogger.logger.info(encode_wrap('%s, 下一页:%d, 暂停%ds' % (buttonText,(i+2), self.stop)))
                        #print '*'*20, '%s, 下一页:%d, 暂停3s' % (buttonText,(i+2)), '*'*20
                        print '\n'
                        time.sleep(self.stop)

                        items = self.parse_data(driver.page_source, i+2, lengthtype)
                        items_all.extend(items)

                except Exception,e:
                    self.infoLogger.logger.info(encode_wrap('未达到%d页，提前结束' % self.pagecount))


            except Exception,e:
                self.errorLogger.logger.error(encode_wrap(str(e)))


        driver.quit()
        print 'parse phantomjs success '

        return items_all


    # 普通搜索
    def parse_data(self, text, page, lengthType):

        items = []

        try:

            soup = bs(text, 'html5lib')

            source = soup.find("div", attrs={'class':'list_rec mt10 clearfix'})
            if soup:
                titleAndLinks = soup.findAll('a', {'class':'p_txt'})

                #视频链接
                for titleAndLink in titleAndLinks:
                    try:

                        if titleAndLink:

                            item = DataItem()


                            # print '标题:',titleAndLink['title']
                            # print '链接:',titleAndLink['href']
                            item.title = titleAndLink.get_text()
                            item.href = titleAndLink['href']

                            self.infoLogger.logger.info(encode_wrap('标题:' + item.title))
                            self.infoLogger.logger.info(encode_wrap('链接:' + item.href))

                            # durationTag = titleAndLink.find('span', attrs={'class':'new_info'})
                            # if durationTag:
                            #     self.infoLogger.logger.info(encode_wrap('时长:' + durationTag.text))
                            #     #print '时长:',durationTag.text
                            #     item.duration = durationTag.text

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

    video = CNTVVideo()
    video.run(data['key'].get_values())

