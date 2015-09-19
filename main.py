# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import pandas as pd
from video_youku import YoukuVideo
from video_tudou import TudouVideo


if __name__ == "__main__":

    data = pd.read_excel('keys.xlsx', 'Sheet3', index_col=None, na_values=['NA'])
    print data

    video = YoukuVideo()
    video.run(data['key'].get_values())

    video = TudouVideo()
    video.run(data['key'].get_values())

