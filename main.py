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


if __name__ == "__main__":

    #data = pd.read_excel('C:\Users\Administrator\Desktop\Data\keys.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
    data = pd.read_excel('keys.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
    print data


    print sse
    t = raw_input("请确认以上关键字(输入 yes 继续,  其它键退出): ".encode(sse))

    t = t.strip().lower()

    if ( t == 'yes'):

        keys = data['key'].get_values()

        video = YoukuVideo()
        video.filePath = 'C:/Users/Administrator/Desktop/Data/Result/youku_video.xlsx'
        video.run(keys)

        video = TudouVideo()
        video.filePath = 'C:/Users/Administrator/Desktop/Data/Result/tudou_video.xlsx'
        video.run(keys)

        #复制目录
        #shutil.copytree(r'C:\Code\video_spider\data', r'C:\Users\Administrator\Desktop\Data')
        #shutil.copyfile(video.filePath,'C:\Users\Administrator\Desktop\Data\Result' )

    else:
        print '>>>  exit  >>>'
        time.sleep(1)

