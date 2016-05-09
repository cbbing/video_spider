# -*- coding: utf-8 -*-
#!/usr/bin/env python
#抓取优酷搜索结果
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import pandas as pd
from video_soku import SokuVideo

class YoukuVideo(SokuVideo):
    def __init__(self):
        SokuVideo.__init__(self)
        self.engine = '优酷'
        self.site = 'youku'
        self.album_url = 'http://www.soku.com/search_video/q_key' #专辑的url
        self.general_url = 'http://www.soku.com/search_video/q_key_orderby_1_lengthtype_tid?site=14&page=pid' #普通搜索的url
        self.filePath = 'youku_video'

        self.timelengthDict = {0:'不限', 1:'0-10分钟', 2:'10-30分钟', 3:'30-60分钟', 4:'60分钟以上'} #时长类型对应网页中的按钮文字


if __name__=='__main__':

    data = pd.read_excel('keys.xlsx', u'优酷网', index_col=None, na_values=['NA'])
    print data

    keys = data['key'].get_values()

    youkuVideo = YoukuVideo()
    youkuVideo.run(keys[:1])
    #youkuVideo.run(['明若晓溪','旋风少女','偶像来了'])
    #key = '快乐大本营'
    #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))


