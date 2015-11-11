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

from bs4 import BeautifulSoup as bs
import pandas as pd
from util.MyLogger import Logger
from util.codeConvert import *
from selenium import webdriver

from init import *

from sqlalchemy import create_engine
import MySQLdb
engine_sql = create_engine('mysql+mysqldb://shipin:AAaa0924@shipinjiankong.mysql.rds.aliyuncs.com:3306/shipinjiankong',
                       connect_args={'charset':'utf8'})
conn=MySQLdb.connect(host="shipinjiankong.mysql.rds.aliyuncs.com",user="shipin",passwd="AAaa0924",db="shipinjiankong",charset="utf8")

class BaseVideo:
    def __init__(self):

        cf = ConfigParser.ConfigParser()
        print os.getcwd()
        cf.read(config_file_path)

        self.dfs = []
        self.items = []
        self.pagecount = int(cf.get("general","page_count"))
        self.filePath = ''
        self.engine = ''

        self.stop = 3 # 暂停3s

        self.infoLogger = Logger(logname=dir_log+'info_base.log', logger='I')
        self.errorLogger = Logger(logname=dir_log+'error_base.log', logger='E')



    def create_data(self, key):
        df = DataFrame({'Title':[item.title for item in self.items],
                        'Href':[item.href for item in self.items],
                        'Duration':[item.duration for item in self.items],
                        'Page':[item.page for item in self.items],
                        'DurationType':[item.durationType for item in self.items]
                        },
                       columns=['Title', 'Href', 'Duration', 'DurationType', 'Page'])
        print df[:10]
        df['Time'] = GetNowTime()
        df['Engine'] = self.engine
        df['Source'] = df['Href'].apply(lambda x : self.get_video_source(x))

        #匹配度
        f = lambda x : '完全匹配' if key in x else '不匹配'
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

        self.infoLogger.logger.info(encode_wrap('去重前，总个数:%d' % len(df)))
        df = df.drop_duplicates(['Href'])
        #过滤无效的视频
        #self.filter_involt_video(df)
        self.infoLogger.logger.info(encode_wrap('去重后，总个数:%d' % len(df)))
        self.dfs.append((key, df))


    def filter_short_video(self):
        items_temp = []
        for item in self.items:
            if len(str(item.duration)) > 0:

                mustFilter = True
                splits = str(item.duration).split(':')
                if len(splits) == 2:
                    minute = int(splits[0])
                    if minute >= 10:
                        mustFilter = False
                elif len(splits) == 3:
                    mustFilter = False

                if not mustFilter:
                    items_temp.append(item)
            else:
                items_temp.append(item)

        self.items = items_temp

    def filter_involt_video(self, df):

        driver = webdriver.Firefox()

        for i in range(len(df)):
            se = df.loc[i]
            print se
            driver.get(se['Href'])

            #过滤无效视频
            if 'error' in driver.current_url or '好像不能看了' in driver.page_source:
                print se
                df.drop(se.name)


        driver.quit()

    def save_data(self):
        self.data_to_excel()
        self.data_to_sql()

    def data_to_excel(self):

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
        self.infoLogger.logger.info(encode_wrap('写入excel完成'))


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
                self.infoLogger.logger.info('写入mysql, %s, 数量:%s' %(key, len(df)))
                df.to_sql(mysql_result_table, engine_sql, if_exists='append', index=False)



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
                      'ku6':'酷6',
                      'fun':'风行网',
                      'kankan':'响巢看看',
                      'baofeng':'暴风影音',
                      'baomihua':'爆米花',
                      'baidu':'百度'}

        try:
            m = re.search(r"\.(\w*?)\.[com|cn]", url)  #\w匹配[a-zA-z0-9]
            key = m.group(1) #如hunantv
            return dictSource[key]
        except Exception, e:
            self.errorLogger.logger.error(encode_wrap(str(e)))
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

    data = pd.read_excel('keys.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
    print data.columns

    youkuVideo = BaseVideo()
    youkuVideo.run(data['key'].get_values())

    #key = '快乐大本营'
    #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))



