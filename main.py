# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
sse = sys.stdout.encoding

from multiprocessing.dummy import Pool as ThreadPool

import time
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
from util.MyLogger import InfoLogger

import platform

def run(index):

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
        print '编号:%d, 运行出错' % index

if __name__ == "__main__":

    systemName = platform.system()
    key_path = 'keys.xlsx'
    if systemName == 'Windows':
        key_path = 'C:\Users\Administrator\Desktop\Data\keys.xlsx'

    #data = pd.read_excel('C:\Users\Administrator\Desktop\Data\keys.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
    data = pd.read_excel(key_path, 'Sheet1', index_col=None, na_values=['NA'])
    print data

    t = raw_input("请确认以上关键字(输入 yes 继续,  其它键退出): ".encode(sse))

    t = t.strip().lower()

    if ( t == 'yes'):

        keys = data['key'].get_values()

        systemName = platform.system()
        if systemName == 'Windows':
            dir_path = 'C:/Users/Administrator/Desktop/Data/Result/'
        else:
            dir_path = './data/'


        indexs = range(1, 12)
        pool = ThreadPool(processes=11)
        pool.map(run, indexs)
        pool.close()
        pool.join()

    else:
        print '>>>  exit  >>>'
        time.sleep(1)

