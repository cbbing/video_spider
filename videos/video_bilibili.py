# -*- coding: utf-8 -*-
#!/usr/bin/env python
#抓取163video搜索结果
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

class BilibiliVideo(BaseVideo):
    def __init__(self):
        BaseVideo.__init__(self)
        self.engine = '哗哩哗哩'
        self.site = 'bilibili'
        #self.album_url = 'http://so.v.163.com/search/000-0-0000-1-1-0-{key}/' #专辑的url
        self.general_url = 'http://search.bilibili.com/all?keyword={key}' #普通搜索的url
        self.filePath = 'bilibili_video'

        self.timelengthDict = {0:'全部时长', 1:'10分钟以下', 2:'10-30分钟', 3:'30-60分钟', 4:'60分钟以上'} #时长类型对应网页中的按钮文字

        #self.infoLogger = Logger(logname=dir_log+'info_56(' + GetNowDate()+ ').log', logger='I')
        #self.errorLogger = Logger(logname=dir_log+'error_56(' + GetNowDate()+ ').log', logger='E')

    @fn_timer_
    def run(self, keys):

        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        lengthtypes = cf.get(self.site,"lengthtype")
        if len(lengthtypes.strip('[').strip(']')) == 0:
            print encode_wrap('配置为不运行')
            return

        self.run_keys(keys)


    def search(self, key):

        items_all = []

        #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))

        url = self.general_url.format(key=key)

        print 'start phantomjs', encode_wrap(url)

        driver = webdriver.Firefox()
        driver.get(url)

        driver.maximize_window()

        # driver.get_screenshot_as_file("show.png")
        #
        # f = open('./data/data.html','w')
        # f.write(driver.page_source)
        # f.close()

        #普通
        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        lengthtypes = cf.get("bilibili","lengthtype")
        lengthtypes = lengthtypes.strip('[').strip(']').split(',')
        for lengthtype in lengthtypes:

            try:
                buttonText = self.timelengthDict[int(lengthtype)]

                # 模拟点击
                driver.find_element_by_link_text(buttonText).click()


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
        print 'item len:',len(items_all)
        return items_all


    # 普通搜索
    def parse_data(self, text, page, lengthType):

        items = []

        try:

            soup = bs(text, 'html5lib')

            if soup:
                titleAndLinks = soup.findAll('li', {'class':'video matrix '})

                #视频链接
                for titleAndLink in titleAndLinks:
                    try:

                        if titleAndLink:

                            data_a = titleAndLink.find('a', {'class':'title'})
                            if not data_a:
                                continue

                            item = DataItem()

                            item.title = data_a['title']
                            item.href = data_a['href']

                            #self.infoLogger.logger.info(encode_wrap('标题:' + item.title))
                            #self.infoLogger.logger.info(encode_wrap('链接:' + item.href))

                            durationTag = titleAndLink.find('span', attrs={'class':'so-imgTag_rb'})
                            if durationTag:
                                #print '时长:',durationTag.text
                                item.duration = durationTag.text.strip()

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

    video = BilibiliVideo()
    video.run(data['key'].get_values()[:100])

    #key = '快乐大本营'
    #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))


