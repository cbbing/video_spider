# -*- coding: utf-8 -*-
#!/usr/bin/env python
#抓取优酷搜索结果
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import pandas as pd
from video_soku import SokuVideo

class TudouVideo(SokuVideo):
    def __init__(self):
        SokuVideo.__init__(self)

        self.album_url = 'http://www.soku.com/t/nisearch/key/_cid__time__sort_score_display_album?site=1' #专辑的url
        self.general_url = 'http://www.soku.com/t/nisearch/key/_cid__time_tid_sort_score_display_album?site=1&page=pid' #普通搜索的url
        self.filePath = './data/tudou_video'

        self.timelengthDict = {0:'不限', 100:'0-10分钟', 110:'10-30分钟', 130:'30-60分钟', 160:'60分钟以上'} #时长类型对应网页中的按钮文字
        self.web = 'tudou'


if __name__=='__main__':
    #key = raw_input('输入搜索关键字:')

    data = pd.read_excel('keys.xlsx', 'Sheet2', index_col=None, na_values=['NA'])
    print data

    youkuVideo = TudouVideo()
    youkuVideo.run(data['key'].get_values())
    #youkuVideo.run(['明若晓溪','旋风少女','偶像来了'])
    #key = '快乐大本营'
    #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))


