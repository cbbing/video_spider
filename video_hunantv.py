# -*- coding: utf-8 -*-
#!/usr/bin/env python
#抓取芒果TV搜索结果
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



class HuNanTVVideo(BaseVideo):
    def __init__(self):
        BaseVideo.__init__(self)
        self.engine = '芒果TV'
        self.site = 'hunantv'
        self.general_url = 'http://so.hunantv.com/so/k-{key}#' #普通搜索的url
        self.filePath = 'hunantv_video'

        self.timelengthDict = {0:'不限', 1:'0-10分钟', 2:'10-30分钟', 3:'30-60分钟', 4:'60分钟以上'} #时长类型对应网页中的按钮文字

        #self.infoLogger = Logger(logname=dir_log+'info_hunantv(' + GetNowDate()+ ').log', logger='I')
        #self.errorLogger = Logger(logname=dir_log+'error_hunantv(' + GetNowDate()+ ').log', logger='E')


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

        url = self.general_url.format(key=key)

        print 'start phantomjs', encode_wrap(url)

        #driver = webdriver.PhantomJS()
        driver = webdriver.Firefox()
        driver.get(url)

        driver.maximize_window()
        # siz = driver.get_window_size()
        # driver.set_window_size(siz['width'], siz['height']*2)

        driver.get_screenshot_as_file("show.png")

        f = open('./data/data.html','w')
        f.write(driver.page_source)
        f.close()

        #普通
        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        lengthtypes = cf.get("hunantv","lengthtype")
        lengthtypes = lengthtypes.strip('[').strip(']').split(',')
        for lengthtype in lengthtypes:

            try:
                buttonText = self.timelengthDict[0]
                #buttonText = self.timelengthDict[int(lengthtype)]

                #js = "var sel=document.getElementById('durationlist');sel.options[1].onclick()"
                #driver.execute_script(js)

                #鼠标悬停
                # durationBtn = driver.find_elements_by_xpath('//a[@id="duration-btn"]')
                # print durationBtn.count()
                # test= driver.find_element_by_link_text('综艺')
                # action = webdriver.ActionChains(driver)
                # action.move_to_element(durationBtn)
                # #action.click_and_hold().perform()
                # action.click()
                # action.perform()
                #
                # # 模拟点击
                # driver.find_element_by_link_text(buttonText).click()


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
                        #print '*'*20, '%s, 下一页:%d, 暂停3s' % (buttonText,(i+2)), '*'*20
                        print '\n'
                        time.sleep(self.stop)

                        items = self.parse_data(driver.page_source, i+2, lengthtype)
                        items_all.extend(items)

                except Exception,e:
                    infoLogger.logger.info('未达到%d页，提前结束' % self.pagecount)


            except Exception,e:
                errorLogger.logger.error(str(e))


        driver.quit()
        print 'parse phantomjs success '

        return items_all


    # 普通搜索
    def parse_data(self, text, page, lengthType):

        items = []

        try:

            soup = bs(text, 'html5lib')

            source = soup.find("div", attrs={'class':'search-resultlist'})
            if source:
                titleAndLinks = source.findAll('div', {'class':'result-box'})

                #视频链接
                for titleAndLink in titleAndLinks:
                    try:

                        if titleAndLink:

                            data_a = titleAndLink.find('a')
                            if not data_a:
                                continue

                            item = DataItem()

                            item.title = data_a.get_text()
                            item.href = data_a['href']

                            #self.infoLogger.logger.info(encode_wrap('标题:' + item.title))
                            #self.infoLogger.logger.info(encode_wrap('链接:' + item.href))

                            # durationTag = titleAndLink.find('span', attrs={'class':'rb'})
                            # if durationTag:
                            #     self.infoLogger.logger.info(encode_wrap('时长:' + durationTag.text))
                            #     #print '时长:',durationTag.text
                            #     item.duration = durationTag.text

                            item.page = page
                            try:
                                item.durationType = self.timelengthDict[int(lengthType)]
                            except Exception,e:
                                errorLogger.logger.error('未找到对应的时长类型!')

                            items.append(item)

                    except Exception,e:
                        errorLogger.logger.error(str(e))
                        #print str(e)

        except Exception, e:
            errorLogger.logger.error(str(e))

        return items

if __name__=='__main__':
    #key = raw_input('输入搜索关键字:')

    data = pd.read_excel('keys.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
    print data

    video = HuNanTVVideo()
    video.run(data['key'].get_values())

