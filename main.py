# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
sse = sys.stdout.encoding

from multiprocessing.dummy import Pool as ThreadPool

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

import platform

def run(index):

    systemName = platform.system()

    if systemName == 'Windows':
        dir_path = 'C:/Users/Administrator/Desktop/Data/Result/'
    else:
        dir_path = './data/'

    key_path = 'keys.xlsx'

    if systemName == 'Windows':
        key_path = 'C:\Users\Administrator\Desktop\Data\keys.xlsx'
    data = pd.read_excel(key_path, 'Sheet1', index_col=None, na_values=['NA'])
    keys = data['key'].get_values()

    try:
        if index == 1:
            #1
            print 'begin youku'
            video = YoukuVideo()
            video.filePath = dir_path + 'youku_video.xlsx'
            video.run(keys)

        elif index == 2:
            #2
            print 'begin tudou'
            video = TudouVideo()
            video.filePath = dir_path + 'tudou_video.xlsx'
            video.run(keys)

        elif index == 3:
            #3
            print 'begin sina'
            video = SinaVideo()
            video.filePath = dir_path + 'sina_video.xlsx'
            video.run(keys)

        elif index == 4:
            #4
            print 'begin sohu'
            video = SouhuVideo()
            video.filePath = dir_path + 'sohu_video.xlsx'
            video.run(keys)

        elif index == 5:
            #5
            print 'begin qq'
            video = QQVideo()
            video.filePath = dir_path + 'qq_video.xlsx'
            video.run(keys)

        elif index == 6:
            #6
            print 'begin iqiyi'
            video = IQiYiVideo()
            video.filePath = dir_path + 'iqiyi_video.xlsx'
            video.run(keys)

        elif index == 7:
            #7
            print 'begin letv'
            video = LetvVideo()
            video.filePath = dir_path + 'letv_video.xlsx'
            video.run(keys)

        elif index == 8:
            #8
            print 'begin huashu'
            video = HuashuVideo()
            video.filePath = dir_path + 'huashu_video.xlsx'
            video.run(keys)

        elif index == 9:
            #9
            print 'begin fun'
            video = FunVideo()
            video.filePath = dir_path + 'fun_video.xlsx'
            video.run(keys)

        elif index == 10:
            #10
            print 'begin kankan'
            video = KankanVideo()
            video.filePath = dir_path + 'kankan_video.xlsx'
            video.run(keys)

        elif index == 11:
            #11
            print 'begin baofeng'
            video = BaofengVideo()
            video.filePath = dir_path + 'baofeng_video.xlsx'
            video.run(keys)
    except Exception, e:
        print encode_wrap('编号:%d, 运行出错' % index), str(e)

def run_all():

    systemName = platform.system()
    print os.getcwd()
    key_path = 'keys.xlsx'

    if systemName == 'Windows':
        key_path = 'C:\Users\Administrator\Desktop\Data\keys.xlsx'

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
    pool = ThreadPool(processes=1)
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
             '11：暴风影音\n(输入数字):'
    raw = raw_input(encode_wrap(prompt))
    try:
        run(int(raw))
    except Exception, e:
        print encode_wrap('请输入正确的序号')


if __name__ == "__main__":
    print "arg len:", len(sys.argv)
    for arg in sys.argv:
        print arg, type(arg)
    if len(sys.argv) == 2:
        type = sys.argv[1]

    if len(sys.argv) > 1:
        run_each()
    else:
        run_all()