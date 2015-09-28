# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
sse = sys.stdout.encoding

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
from video_baidu import BaiduVideo
from util.MyLogger import InfoLogger

import platform


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

        #1
        InfoLogger.addLog('begin youku')
        video = YoukuVideo()
        video.filePath = dir_path + 'youku_video.xlsx'
        video.run(keys)

        #2
        InfoLogger.addLog('begin tudou')
        video = TudouVideo()
        video.filePath = dir_path + 'tudou_video.xlsx'
        video.run(keys)

        #3
        InfoLogger.addLog('begin sina')
        video = SinaVideo()
        video.filePath = dir_path + 'sina_video.xlsx'
        video.run(keys)

        #4
        InfoLogger.addLog('begin sohu')
        video = SouhuVideo()
        video.filePath = dir_path + 'sohu_video.xlsx'
        video.run(keys)

        #5
        InfoLogger.addLog('begin qq')
        video = QQVideo()
        video.filePath = dir_path + 'qq_video.xlsx'
        video.run(keys)

        #6
        InfoLogger.addLog('begin iqiyi')
        video = IQiYiVideo()
        video.filePath = dir_path + 'iqiyi_video.xlsx'
        video.run(keys)

        #7
        InfoLogger.addLog('begin letv')
        video = LetvVideo()
        video.filePath = dir_path + 'letv_video.xlsx'
        video.run(keys)

        #8
        InfoLogger.addLog('begin huashu')
        video = HuashuVideo()
        video.filePath = dir_path + 'huashu_video.xlsx'
        video.run(keys)


    else:
        print '>>>  exit  >>>'
        time.sleep(1)

