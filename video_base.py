# -*- coding: utf-8 -*-
#!/usr/bin/env python
#抓取优酷搜索结果
import sys, os
reload(sys)
sys.setdefaultencoding("utf-8")

import time
import re
import ConfigParser
from pandas import Series, DataFrame
import random
import requests

from bs4 import BeautifulSoup as bs
import pandas as pd
from util.MyLogger import Logger
from util.code_convert import *
from selenium import webdriver
from retrying import retry
from multiprocessing.dummy import Pool as ThreadPool

from init import *
from IPProxy.ip_proxy import IP_Proxy

from sqlalchemy import create_engine
import MySQLdb
from util.helper import fn_timer as fn_timer_
from util.webHelper import get_ip_dataframe
from Post.check_404 import check_404

engine_sql = create_engine('mysql+mysqldb://shipin:AAaa0924@shipinjiankong.mysql.rds.aliyuncs.com:3306/shipinjiankong',
                       connect_args={'charset':'utf8'})
conn=MySQLdb.connect(host="shipinjiankong.mysql.rds.aliyuncs.com",user="shipin",passwd="AAaa0924",db="shipinjiankong",charset="utf8")

class BaseVideo:
    def __init__(self):

        cf = ConfigParser.ConfigParser()
        print os.getcwd()
        cf.read(config_file_path)

        self.dfs = []
        #self.items = []
        self.pagecount = int(cf.get("general","page_count"))
        self.filePath = ''
        self.engine = ''
        self.site = ''

        self.stop = 3 # 暂停3s

        self.infoLogger = Logger(logname=dir_log+'info_base(' + GetNowDate()+ ').log', logger='I')
        self.errorLogger = Logger(logname=dir_log+'error_base(' + GetNowDate()+ ').log', logger='E')

        self.df_ip = get_ip_dataframe()
        # ip_file = "./data/ip_proxy_%s.csv" % GetNowDate()
        # try:
        #     self.df_ip = pd.read_csv(ip_file)
        # except:
        #     print 'not exist:%s, get it now!' % ip_file
        #     self.update_ip_data()


    # 更新IP代理库
    def update_ip_data(self):
        ip_file = "./data/ip_proxy_%s.csv" % GetNowDate()
        ip_proxy = IP_Proxy()
        ip_proxy.run()
        self.df_ip = pd.read_csv(ip_file)

    # 获取IP代理地址(随机)
    def get_proxies(self):

        if len(self.df_ip) > 0:
            #print len(self.df_ip)
            index = random.randint(0, len(self.df_ip))
            http = self.df_ip.ix[index, 'Type']
            http = str(http).lower()
            ip = self.df_ip.ix[index, 'IP']
            port = self.df_ip.ix[index, 'Port']
            ip_proxy = "%s://%s:%s" % (http, ip, port)
            proxies = {http:ip_proxy}
            print proxies
            return proxies
        else:
            return {}


    # requests使用代理请求
    @retry(stop_max_attempt_number=100)
    def get_requests(self, url):

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}

        proxy = self.get_proxies()

        r = requests.get(url, proxies=proxy, headers=headers, timeout=5)
        output = 'Code:{1}  Proxy:{2}  Url:{0}  '.format(url, r.status_code, proxy)
        output = encode_wrap(output)

        #self.errorLogger.logger.error(output)

        if int(r.status_code) != 200:
            raise Exception('request fail')



        return r

    # 单线程运行keys
    def run_keys(self, keys):
        for key in keys:
            self.run_key(key)

    # 多线程运行keys
    @fn_timer_
    def run_keys_multithreading(self, keys):

        #多线程
        pool = ThreadPool(processes=20)
        pool.map(self.run_key, keys)
        pool.close()
        pool.join()

        # #保存数据
        #self.save_data()

    # 运行单个key
    def run_key(self, key):
        try:
            # 初始化
            #self.items = []

            #搜索
            items = self.search(key)

            #创建dataframe
            df = self.create_data(key, items)

            # 失效链接判断
            # f = lambda url : '有效' if check_404(url) else '无效'
            # df['Validity'] = df['Href'].apply(f)
            # print df['Validity']

            self.data_to_sql_by_key(key, df)

        except Exception,e:
            self.errorLogger.logger.info('unfinish:' + self.site +'_' + key + "_" + str(e))
            self.data_to_unfinish_file( key)

    # 运行未完成的key
    def run_unfinished_keys(self, keys_total, start_time):
        v_source = self.get_video_source('.'+self.site+'.com')
        sql = "select distinct VideoKey from %s where Time>'%s' and Source='%s'" % (mysql_result_table, start_time, v_source)
        df = pd.read_sql_query(sql, engine_sql)
        if len(df) > 0:
            keys_finished = df['VideoKey'].get_values()
            keys_unfinished = [key for key in set(keys_total).difference(set(keys_finished))]
            self.run_keys_multithreading(keys_unfinished)

    def search(key):
        return []

    def create_data(self, key, items):
        df = DataFrame({'Title':[item.title for item in items],
                        'Href':[item.href for item in items],
                        'Duration':[item.duration for item in items],
                        'Page':[item.page for item in items],
                        'DurationType':[item.durationType for item in items]
                        },
                       columns=['Title', 'Href', 'Duration', 'DurationType', 'Page'])
        print df[:10]
        df['Time'] = GetNowTime()
        df['Engine'] = self.engine
        df['Source'] = df['Href'].apply(lambda x : self.get_video_source(x))

        #匹配度
        def is_key_match(key, x):
            for ch in key:
                if not ch in x:
                    return False
            return True
        f = lambda x : '完全匹配' if is_key_match(key, x) else '不匹配'

        #f = lambda x : '完全匹配' if key in x else '不匹配'

        df['KeyMatch'] = df['Title'].apply(f)
        df = df.sort_index(by='KeyMatch', ascending=False)

        #过滤“排除关键词列表”
        try:
            print '排除关键词前：', len(df)
            data = pd.read_excel(key_path, 'Sheet1', index_col=None, na_values=['NA'])
            keys = data['excludeKey'].get_values()
            print keys
            keys = ','.join(keys)
            keys = keys.replace('，', ',')
            keys = keys.split(',')

            def sub_f(x):
                for key in keys:
                    if key.strip() in x:
                        return False
                return True
            f1 = lambda x : sub_f(x)
            df = df[df['Title'].apply(f1)]

            print '排除关键词后：', len(df)
        except Exception,e:
            print e

        # if df['Duration'].any() == '':
        #     df = df.drop('Duration', axis=1)

        #df['Title'] = df['Title'].apply(lambda x : str(x).replace('【', '[').replace('】',']').replace('《','<').replace('》','>')) #([u'【',u'】',u'《',u'》'],['[',']','<','>'])
        #df['Title'] = df['Title'].apply(lambda x : str(x).decode('gbk','ignore').encode('utf8'))
        print df[:10]

        #self.infoLogger.logger.info(encode_wrap('%s:%s:去重前，总个数:%d' % (self.site, key, len(df))))
        print encode_wrap('%s:%s:去重前，总个数:%d' % (self.site, key, len(df)))
        df = df.drop_duplicates(['Href'])

        #过滤无效的视频
        #self.filter_involt_video(df)

        #self.infoLogger.logger.info(encode_wrap('%s:%s:去重后，总个数:%d' % (self.site, key, len(df))))
        print encode_wrap('%s:%s:去重后，总个数:%d' % (self.site, key, len(df)))
        self.dfs.append((key, df))
        return df


    # def filter_short_video(self):
    #     items_temp = []
    #     for item in self.items:
    #         if len(str(item.duration)) > 0:
    #
    #             mustFilter = True
    #             splits = str(item.duration).split(':')
    #             if len(splits) == 2:
    #                 minute = int(splits[0])
    #                 if minute >= 10:
    #                     mustFilter = False
    #             elif len(splits) == 3:
    #                 mustFilter = False
    #
    #             if not mustFilter:
    #                 items_temp.append(item)
    #         else:
    #             items_temp.append(item)
    #
    #     self.items = items_temp

    def filter_involt_video(self, df):
        try:
            # 失效链接判断
            if self.site == 'youku':

                # f = lambda url : '有效' if check_404(url) else '无效'
                # df['Validity'] = df['Href'].apply(f)
                # print df['Validity']

                driver = webdriver.PhantomJS()
                #driver = webdriver.Firefox()

                for i in range(len(df)):
                    se = df.loc[i]
                    print se
                    if not check_404(se['Href'], driver): #删除无效视频
                        print se
                        df.drop(se.name)

                    #过滤无效视频
                    # if 'error' in driver.current_url or '好像不能看了' in driver.page_source:
                    #     print se
                    #     df.drop(se.name)


                driver.quit()

        except Exception,e:
            print e

    def save_data(self):
        self.data_to_excel()
        #self.data_to_sql()

    def data_to_excel(self):
        try:
            now_data = GetNowDate()
            if not os.path.exists(dir_path + now_data):
                os.mkdir(dir_path + now_data)

            now_time = GetNowTim3()
            file_name = dir_path + now_data + '/' + self.filePath + '(' + now_time + ').xlsx'

            with pd.ExcelWriter(file_name) as writer:
                for key, df in self.dfs:
                    df.to_excel(writer, sheet_name=key)
                    #df.to_csv("./data/letv_video.csv")
                    #break
            #self.infoLogger.logger.info(encode_wrap('%s:写入excel完成' % self.site))
            print encode_wrap('%s:写入excel完成' % self.site)
        except:
            self.errorLogger.logger.info(encode_wrap('%s:写入excel fail' % self.site))


    def data_to_sql(self):

        for key, df in self.dfs:
            df['VideoKey'] = key
            print df[:10]
            try:
                sql = "select Href from %s where VideoKey='%s' and Engine='%s'" % (mysql_result_table, key, self.engine)
                #sql = "select Href from %s" % mysql_result_table
                df_exist = pd.read_sql_query(sql, engine_sql)
                if len(df_exist) > 0:
                    hrefs = df_exist['Href'].get_values()
                    df = df.drop([ix for ix, row in df.iterrows() if row['Href'] in hrefs])
            except Exception, e:
                print e

            if len(df)>0:
                #self.infoLogger.logger.info('写入mysql, %s:%s, 数量:%s' %(self.site, key, len(df)))
                print encode_wrap('写入mysql, %s:%s, 数量:%s' %(self.site, key, len(df)))
                df.to_sql(mysql_result_table, engine_sql, if_exists='append', index=False)

    def data_to_sql_by_key(self, key, df):
        df['VideoKey'] = key
        print df[:10]
        try:
            sql = "select Href from %s where VideoKey='%s' and Engine='%s'" % (mysql_result_table, key, self.engine)
            #sql = "select Href from %s" % mysql_result_table
            df_exist = pd.read_sql_query(sql, engine_sql)
            if len(df_exist) > 0:
                hrefs = df_exist['Href'].get_values()
                df = df.drop([ix for ix, row in df.iterrows() if row['Href'] in hrefs])
        except Exception, e:
            print e

        if len(df)>0:
            #self.infoLogger.logger.info('写入mysql, %s:%s, 数量:%s' %(self.site, key, len(df)))
            print encode_wrap('写入mysql, %s:%s, 数量:%s' %(self.site, key, len(df)))
            df.to_sql(mysql_result_table, engine_sql, if_exists='append', index=False)

    def data_to_unfinish_file(self, key):
        try:
            with open(dir_log + 'unfinish_list.txt', 'a') as f:
                s_info = self.site + ',' + key + ',' + GetNowTime() + '\n'
                f.write(s_info)
                f.close()
        except Exception, e:
            info = '{0}:{1}:{2}:{3}'.format(self.site, key,"write_to_unfinish_file fail!", str(e))
            self.errorLogger.logger.error(encode_wrap(info))

    # 判断视频来源
    def get_video_source(self, url):
        dictSource = {'hunantv':'芒果TV',
                      'youku':'优酷',
                      'tudou':'土豆',
                      'iqiyi':'爱奇艺',
                      'letv':'乐视',
                      'sina':'新浪视频',
                      'sohu':'搜狐视频',
                      'qq':'腾讯视频',
                      'wasu':'华数',
                      'ifeng':'凤凰视频',
                      '56':'56',
                      '1905':'1905电影网',
                      'kankan':'响巢看看',
                      'cntv':'CNTV',
                      'cctv':'CCTV',
                      'ku6':'酷6',
                      'fun':'风行网',
                      'kankan':'响巢看看',
                      'baofeng':'暴风影音',
                      'baomihua':'爆米花',
                      'pptv':'PPTV',
                      'tv189':'TV189',
                      'baidu':'百度'}

        try:
            m = re.search(r"\.(\w*?)\.[com|cn]", url)  #\w匹配[a-zA-z0-9]
            key = m.group(1) #如hunantv
            return dictSource[key]
        except Exception, e:
            #self.errorLogger.logger.error(encode_wrap(str(e)))
            return ''


class DataItem:
    def __init__(self):
        self.title = ''
        self.href = ''
        self.duration = ''
        self.page = 0 #页码
        self.durationType = '' #时长类型


if __name__=='__main__':
    #key = raw_input('输入搜索关键字:')

    # data = pd.read_excel('keys.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
    # print data.columns

    # youkuVideo = BaseVideo()
    # youkuVideo.run(data['key'].get_values())

    #key = '快乐大本营'
    #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))

    print check_contain_chinese('中国')
    check_str = '跟班×服务Servant×Service'
    for ch in check_str.decode('utf-8'):
        print ch

