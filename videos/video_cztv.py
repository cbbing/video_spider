# -*- coding: utf-8 -*-
#!/usr/bin/env python
# 新蓝网
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from video_base import *

class CZTVVideo(BaseVideo):
    def __init__(self):
        BaseVideo.__init__(self)
        self.engine = '新蓝网'
        self.site = 'cztv'
        self.album_url = '' #专辑的url
        self.general_url = 'http://search.cztv.com/?key={key}&sort=time&&page={pid}' #普通搜索的url
        #self.filePath = 'ku_video'

        #self.timelengthDict = {0:'全部', 1:'10分钟以下', 2:'10-30分钟', 3:'30-60分钟', 4:'60分钟以上'} #时长类型对应网页中的按钮文字

    @fn_timer_
    def run(self, keys):

        start_time = GetNowTime()
        self.run_keys(keys)
        #self.run_keys_multithreading(keys)

        #重试运行三次
        # for _ in range(0, 3):
        #     self.run_unfinished_keys(keys, start_time)


    def search(self, key):

        items_all = []

        # 普通
        lengthtypes = [1]
        for lengthtype in lengthtypes:

            for i in range(self.pagecount):
                url = self.general_url.format(key=key, pid=i+1)
                r = self.get_requests(url)
                r.encoding = 'utf8'

                items = self.parse_data(r.text, i+1, lengthtype, url)

                if items:
                    items_all.extend(items)
                else:
                    break

        return items_all

    # 普通
    def parse_data(self, text, page, legth_type, url):

        items = []

        try:
            soup = bs(text, 'lxml')

            #视频链接-全部结果
            dramaList = soup.find_all('h1')
            for drama in dramaList:

                area_a = drama.find('a')
                if not area_a:
                    continue

                item = DataItem()
                item.title = area_a.text
                item.href = area_a['href']

                durationTag = area_a.find('span', attrs={'class':'ckl_tim'})
                if durationTag:
                    item.duration = durationTag.text.strip()

                item.page = page
                # try:
                #     item.durationType = self.timelengthDict[int(legth_type)]
                # except Exception,e:
                #     print encode_wrap('未找到对应的时长类型!')

                items.append(item)
        except Exception,e:
            r.lpushx(r_video_key, self.site+"||"+url)
            print e

        return items

if __name__=='__main__':
    #key = raw_input('输入搜索关键字:')

    data = pd.read_excel('keys.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
    print data

    video = CZTVVideo()
    video.run(data['key'].get_values()[:100])

    #key = '快乐大本营'
    #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))


