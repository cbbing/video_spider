# -*- coding: utf-8 -*-
#!/usr/bin/env python
#抓取weibo video搜索结果
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import pickle
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from video_base import *
from util.webHelper import get_web_driver

class WeiboVideo(BaseVideo):

    dir_temp = 'data/cookie/'

    def __init__(self):
        BaseVideo.__init__(self)
        self.engine = '新浪微博'
        self.site = 'weibo'
        self.album_url = '' #专辑的url
        self.general_url = 'http://s.weibo.com/' #普通搜索的url
        self.filePath = 'weibo_video'

        self.timelengthDict = {0:'全部', 1:'10分钟以下', 2:'10-30分钟', 3:'30-60分钟', 4:'60分钟以上'} #时长类型对应网页中的按钮文字

        #self.infoLogger = Logger(logname=dir_log+'info_56(' + GetNowDate()+ ').log', logger='I')
        #self.errorLogger = Logger(logname=dir_log+'error_56(' + GetNowDate()+ ').log', logger='E')

    def get_logined_webdriver(self):
        """
        获取登录后的driver
        :return:
        """

        driver = get_web_driver(self.general_url, has_proxy=False)
        WebDriverWait(driver, 10, 0.5).until(EC.presence_of_element_located((By.LINK_TEXT, '登录')))

        driver.find_element_by_link_text('登录').click()
        WebDriverWait(driver, 10, 0.5).until(EC.presence_of_element_located((By.LINK_TEXT, '账号登录')))

        driver.find_element_by_link_text('账号登录').click()
        WebDriverWait(driver, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//input[@name="username"]')))

        driver.find_element_by_xpath('//input[@name="username"]').clear()
        driver.find_element_by_xpath('//input[@name="password"]').clear()
        driver.find_element_by_xpath('//input[@name="username"]').send_keys('18410182275')
        driver.find_element_by_xpath('//input[@name="password"]').send_keys('12356789')

        driver.find_element_by_xpath('//div[@class="item_btn"]').click()
        time.sleep(3)
        return driver

    def get_cookie(self):
        """
        获取微博cookie
        """

        def get_cookie_from_network():

            driver = get_web_driver(self.general_url, has_proxy=False)
            WebDriverWait(driver, 10, 0.5).until(EC.presence_of_element_located((By.LINK_TEXT, '登录')))

            driver.find_element_by_link_text('登录').click()
            WebDriverWait(driver, 10, 0.5).until(EC.presence_of_element_located((By.LINK_TEXT, '账号登录')))

            driver.find_element_by_link_text('账号登录').click()
            WebDriverWait(driver, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//input[@name="username"]')))

            driver.find_element_by_xpath('//input[@name="username"]').clear()
            driver.find_element_by_xpath('//input[@name="password"]').clear()
            driver.find_element_by_xpath('//input[@name="username"]').send_keys('18410182275')
            driver.find_element_by_xpath('//input[@name="password"]').send_keys('12356789')

            driver.find_element_by_xpath('//div[@class="item_btn"]').click()
            time.sleep(3)
            # 获得 cookie信息
            cookie_list = driver.get_cookies()
            print cookie_list

            # 写入文件 for webdriver
            f = open(self.dir_temp + 'total_weibo.cookie', 'w')
            pickle.dump(cookie_list, f)
            f.close()

            # 写入文件 for requests
            cookie_dict = {}
            for cookie in cookie_list:
                # 写入文件
                f = open(self.dir_temp + cookie['name'] + '.weibo', 'w')
                pickle.dump(cookie, f)
                f.close()

                if cookie.has_key('name') and cookie.has_key('value'):
                    cookie_dict[cookie['name']] = cookie['value']
            driver.quit()
            return cookie_dict

        def get_cookie_from_cache():

            cookie_dict = {}
            for parent, dirnames, filenames in os.walk(self.dir_temp):
                for filename in filenames:
                    if filename.endswith('.weibo'):
                        # print filename
                        f = open(self.dir_temp + filename, 'r')
                        d = pickle.load(f)
                        f.close()

                        if d.has_key('name') and d.has_key('value') and d.has_key('expiry'):
                            cookie_dict[d['name']] = d['value']


            return cookie_dict

        cookie_dict = get_cookie_from_cache()
        if not cookie_dict:
            cookie_dict = get_cookie_from_network()

        # print cookie_dict
        return cookie_dict

    @fn_timer_
    def run(self, keys):


        self.run_keys(keys)
        # self.run_keys_multithreading(keys)

        #重试运行三次
        # for _ in range(0, 3):
        #     self.run_unfinished_keys(keys, start_time)


    def search(self, key):

        items_all = []

        # 普通

        driver = self.get_logined_webdriver()

        # f = open(self.dir_temp + 'total_weibo.cookie', 'r')
        # cookie_list = pickle.load(f)
        # f.close()
        # for cookie in cookie_list:
        #     print cookie
        #     cookie.pop('domain')
        #     #cookie.pop('expiry')
        #
        #     cookie_to = {}
        #     cookie_to['name'] = cookie['name']
        #     cookie_to['value'] = cookie['value']
        #
        #     driver.add_cookie(cookie_to)
        #
        # print driver.get_cookies()

        for page in range(1, self.pagecount+1):
            url = '{}weibo/{}&page={}'.format(self.general_url, key, page)
            driver.get(url)

            items = self.parse_data(driver.page_source, i+1, 0, key)

            if items:
                items_all.extend(items)
            else:
                break

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
    def parse_data(self, text, page, key):

        items = []

        soup = bs(text, 'lxml')

        #视频链接-全部结果
        # tableArea = soup.find('div', {'class':'ssList area'})
        # if not tableArea:
        #     return []

        dramaList = soup.findAll('h3')
        for drama in dramaList:

            try:
                item = DataItem()

                area_a = drama.find('a')
                item.title = area_a.text
                item.href = area_a['href']

                #self.infoLogger.logger.info(encode_wrap('标题:' + item.title ))
                #self.infoLogger.logger.info(encode_wrap('链接:' + item.href))

                durationTag = area_a.find('span', attrs={'class':'maskTx'})
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

if __name__=='__main__':
    #key = raw_input('输入搜索关键字:')

    data = pd.read_excel('keys.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
    print data

    video = WeiboVideo()
    video.get_cookie()
    video.run(data['key'].get_values()[:100])

    #key = '快乐大本营'
    #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))


