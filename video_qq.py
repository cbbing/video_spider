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
        self.general_url = 'http://v.qq.com/search.html?pagetype=3&stj2=search.search&stag=txt.index&ms_key=keys' #普通搜索的url
        self.filePath = './data/qq_video.xlsx'
        self.timelengthDict = {0:'全部', 1:'10分钟以下', 2:'10-30分钟', 3:'30-60分钟', 4:'60分钟以上'} #时长类型对应网页中的按钮文字

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

            print '\n'
            print '*'*20, '暂停10s', '*'*20
            print '\n'
            time.sleep(10)
            break

        #存入excel
        print len(self.dfs)
        self.data_to_excel()

    def search(self, key):

        #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))

        qq_url = self.general_url
        qq_url = qq_url.replace('keys',key)

        print 'start phantomjs'
        print qq_url
        #driver = webdriver.PhantomJS()
        driver = webdriver.Firefox()
        driver.get(qq_url)

        driver.get_screenshot_as_file("show.png")

        f = open('./data/qq.html','w')
        f.write(driver.page_source)
        f.close()

        #专辑
        self.parse_data_album(driver.page_source)

        #普通
        cf = ConfigParser.ConfigParser()
        cf.read("config.ini")
        lengthtypes = cf.get("qq","lengthtype")
        lengthtypes = lengthtypes.strip('[').strip(']').split(',')
        for lengthtype in lengthtypes:

            try:
                buttonText = self.timelengthDict[int(lengthtype)]
                # 模拟点击
                driver.find_element_by_link_text(buttonText).click()

                print '*'*20, '%s, 第一页,暂停3s' % buttonText, '*'*20
                print '\n'
                time.sleep(3)

                #第一页
                self.parse_data(driver.page_source)

                #获取下一页
                try:
                    for i in range(self.pagecount-1):
                        driver.find_element_by_link_text('下一页').click()

                        print '*'*20, '%s, 下一页:%d, 暂停3s' % (buttonText,(i+2)), '*'*20
                        print '\n'
                        time.sleep(3)

                        self.parse_data(driver.page_source)

                except Exception,e:
                    print '未达到%d页，提前结束' % self.pagecount


            except Exception,e:
                print str(e)

        print 'parse phantomjs success'


    # 专辑搜索
    def parse_data_album(self, text):
        try:
            soup = bs(text)

            albumList = soup.findAll('li', attrs={'class':'list_item'})
            for album in albumList:


                #视频链接-专辑(样式一，如偶像来了等综艺节目）
                try:
                    dramaList = album.findAll('div', attrs={'class':'mod_album_titlist_lists video_play_list_cont'})
                    for drama in dramaList:

                        titleAndLinkList = drama.findAll('a')
                        for titleAndLink in titleAndLinkList:

                            item = DataItem()

                            print '标题:',titleAndLink['title']
                            print '链接:',titleAndLink['href']
                            item.title = titleAndLink['title']
                            item.href = titleAndLink['href']

                            self.items.append(item)
                except Exception,e:
                    print "专辑解析出错,", str(e)




                #视频链接-专辑(样式二，如电视连续剧）
                try:
                    drama = album.find('h2', attrs={'class':'result_title'})
                    albumTitle = drama.find('a')['title']

                    dramaList = album.findAll('div', attrs={'class':'mod_album_notitlist_lists video_play_list_cont'})
                    for drama in dramaList:

                        titleAndLinkList = drama.findAll('a')
                        for titleAndLink in titleAndLinkList:

                            item = DataItem()

                            try:
                                print '标题:',albumTitle+'第'+ titleAndLink['data-s-eponum'] +'集'
                                print '链接:',titleAndLink['href']
                                item.title = albumTitle+'第'+ titleAndLink['data-s-eponum'] +'集'
                                item.href = titleAndLink['href']
                                self.items.append(item)
                            except:
                                print '专辑item中不含标题和链接'


                except Exception,e:
                    print "专辑解析出错,", str(e)


                #视频链接-片花
                try:
                    dramaList = album.findAll('div', attrs={'class':'mod_figures_preview'})
                    for drama in dramaList:

                        titleAndLinkList = drama.findAll('a')
                        for titleAndLink in titleAndLinkList:

                            item = DataItem()

                            print '标题:',titleAndLink['title']
                            print '链接:',titleAndLink['href']
                            item.title = titleAndLink['title']
                            item.href = titleAndLink['href']

                            self.items.append(item)
                except Exception, e:
                    print "片花解析出错", str(e)

        except Exception, e:
                print str(e)


    # 普通搜索
    def parse_data(self, text):

        try:

            soup = bs(text)

            source = soup.find("ul", attrs={'class':'mod_list_pic_140 mod_figure_list mod_figure_list_175'})
            if source:
                titleAndLinks = source.findAll('a')

                #视频链接
                for titleAndLink in titleAndLinks:
                    try:

                        if titleAndLink:

                            item = DataItem()

                            print '标题:',titleAndLink['title']
                            print '链接:',titleAndLink['href']
                            item.title = titleAndLink['title']
                            item.href = titleAndLink['href']

                            durationTag = titleAndLink.find('span', attrs={'class':'new_info'})
                            if durationTag:
                                print '时长:',durationTag.text
                                item.duration = durationTag.text

                            self.items.append(item)

                    except Exception,e:
                        print str(e)

        except Exception, e:
            print str(e)

if __name__=='__main__':
    #key = raw_input('输入搜索关键字:')

    data = pd.read_excel('keys.xlsx', 'Sheet2', index_col=None, na_values=['NA'])
    print data

    video = QQVideo()
    video.run(data['key'].get_values())

