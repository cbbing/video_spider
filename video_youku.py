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

        self.album_url = 'http://www.soku.com/search_video/q_key_orderby_1_lengthtype_0?site=14' #专辑的url
        self.general_url = 'http://www.soku.com/search_video/q_key_orderby_1_lengthtype_tid?site=14&page=pid' #普通搜索的url
        self.filePath = './data/youku_video.xlsx'

if __name__=='__main__':

    data = pd.read_excel('keys.xlsx', 'Sheet2', index_col=None, na_values=['NA'])
    print data

    youkuVideo = YoukuVideo()
    youkuVideo.run(data['key'].get_values())
    #youkuVideo.run(['明若晓溪','旋风少女','偶像来了'])
    #key = '快乐大本营'
    #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))


