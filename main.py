# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
sse = sys.stdout.encoding

from multiprocessing.dummy import Pool as ThreadPool

import ConfigParser
import time, os
import shutil
import pandas as pd
from video_youku import YoukuVideo
from video_tudou import TudouVideo
from video_sina import SinaVideo
from video_qq import QQVideo
from video_sohu import SouhuVideo
from video_iqiyi import IQiYiVideo
from video_letv import LetvVideo
from video_huashu import HuashuVideo
from video_fun import FunVideo
from video_kankan import KankanVideo
from video_baofeng import BaofengVideo
from video_baidu import BaiduVideo
from util.codeConvert import encode_wrap

from init import *

def run(index):
    index = int(index)

    systemName = platform.system()

    # if systemName == 'Windows':
    #     dir_path = 'C:/Users/Administrator/Desktop/Data/Result/'
    # else:
    #     dir_path = './data/'
    #
    # key_path = 'keys.xlsx'
    #
    # if systemName == 'Windows':
    #     key_path = 'C:\Users\Administrator\Desktop\Data\keys.xlsx'
    data = pd.read_excel(key_path, 'Sheet1', index_col=None, na_values=['NA'])
    keys = data['key'].get_values()
    print keys

    try:
        if index == 1:
            #1
            print 'begin youku'
            video = YoukuVideo()
            video.filePath = 'youku_video'
            video.run(keys)

        elif index == 2:
            #2
            print 'begin tudou'
            video = TudouVideo()
            video.filePath = 'tudou_video'
            video.run(keys)

        elif index == 3:
            #3
            print 'begin sina'
            video = SinaVideo()
            video.filePath = 'sina_video'
            video.run(keys)

        elif index == 4:
            #4
            print 'begin sohu'
            video = SouhuVideo()
            video.filePath = 'sohu_video'
            video.run(keys)

        elif index == 5:
            #5
            print 'begin qq'
            video = QQVideo()
            video.filePath = 'qq_video'
            video.run(keys)

        elif index == 6:
            #6
            print 'begin iqiyi'
            video = IQiYiVideo()
            video.filePath = 'iqiyi_video'
            video.run(keys)

        elif index == 7:
            #7
            print 'begin letv'
            video = LetvVideo()
            video.filePath = 'letv_video'
            video.run(keys)

        elif index == 8:
            #8
            print 'begin huashu'
            video = HuashuVideo()
            video.filePath = 'huashu_video'
            video.run(keys)

        elif index == 9:
            #9
            print 'begin fun'
            video = FunVideo()
            video.filePath = 'fun_video'
            video.run(keys)

        elif index == 10:
            #10
            print 'begin kankan'
            video = KankanVideo()
            video.filePath = 'kankan_video'
            video.run(keys)

        elif index == 11:
            #11
            print 'begin baofeng'
            video = BaofengVideo()
            video.filePath = 'baofeng_video'
            video.run(keys)



    except Exception, e:
        print encode_wrap('编号:%d, 运行出错' % index), str(e)

def run_all():

    # 百度
    try:
        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        lengthtypes = cf.get("baidu","lengthtype")
        if len(lengthtypes.strip('[').strip(']')) > 0:
            print encode_wrap('运行百度搜索')
            video = BaiduVideo()
            video.run_auto()
    except Exception,e:
        print e
        

    #data = pd.read_excel('C:\Users\Administrator\Desktop\Data\keys.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
    try:
        data = pd.read_excel(key_path, 'Sheet1', index_col=None, na_values=['NA'])
        print data
    except Exception, e:
        print encode_wrap('excel表读取错误，程序退出！')
        return

    print encode_wrap('请确认以上关键字, 10s后继续...')
    time.sleep(10)

    indexs = range(1, 12)
    pool = ThreadPool(processes=4)
    pool.map(run, indexs)
    pool.close()
    pool.join()

def run_each():
    prompt = '请选择序号：\n' \
             '1：优酷\n' \
             '2：土豆\n' \
             '3：新浪视频\n' \
             '4：搜狐视频\n' \
             '5：腾讯视频\n' \
             '6：爱奇艺\n' \
             '7：乐视\n' \
             '8：华数\n' \
             '9：风行\n' \
             '10：响巢看看\n' \
             '11：暴风影音\n' \
             '>>>(输入数字, 单个直接输入数字如1, 多个序号用逗号分隔如: 2,4):'
    raw = raw_input(encode_wrap(prompt))
    try:
        raw = raw.replace('，', ',')
        indexs = raw.split(',')
        for index in indexs:
            index = index.strip()
            if index.isdigit():
                try:
                    run(index)
                except Exception, e:
                    print str(e)
    except Exception, e:
        print encode_wrap('请输入正确的序号')

# 批处理
def run_auto(indexs):
    try:
        indexs = indexs.replace('，', ',')
        indexs = indexs.split(',')
        for index in indexs:
            index = index.strip()
            if index.isdigit():
                run(index)
    except Exception, e:
        print encode_wrap('请输入正确的序号')

if __name__ == "__main__":
    # print "arg len:", len(sys.argv)
    # for arg in sys.argv:
    #     print arg, type(arg)
    # if len(sys.argv) == 2:
    #     type = sys.argv[1]

    if len(sys.argv) == 2:
        run_each()
    elif len(sys.argv) == 3:
        index = sys.argv[2]
        run_auto(index)
    else:
        run_all()