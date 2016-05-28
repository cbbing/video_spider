# -*- coding: utf-8 -*-
#!/usr/bin/env python
# 凤凰视频
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from video_base import *

class IFengVideo(BaseVideo):
    def __init__(self):
        BaseVideo.__init__(self)
        self.engine = '凤凰视频'
        self.site = 'ifeng'
        self.album_url = '' #专辑的url
        self.general_url = 'http://so.v.ifeng.com/video?q={key}&p={pid}' #普通搜索的url
        #self.filePath = 'ku_video'

        #self.timelengthDict = {0:'全部', 1:'10分钟以下', 2:'10-30分钟', 3:'30-60分钟', 4:'60分钟以上'} #时长类型对应网页中的按钮文字

        self.redis_video_key = 'errorlinks::videosearch::ifeng'

    @fn_timer_
    def run(self, keys):

        self.run_keys(keys)
        #self.run_keys_multithreading(keys)

    @fn_timer_
    def run_errorlink_in_redis(self):

        while self.r.llen(self.redis_video_key):
            url = self.r.rpop(self.redis_video_key)
            f = re.search('.*key=(.+)&sort.*', url)
            if f:
                key = f.group(1)

            items = self.parse_data(url)
            df = self.create_data(key, items)
            self.data_to_sql_by_key(key, df)


    def search(self, key):

        items_all = []

        # 普通
        lengthtypes = [1]
        for lengthtype in lengthtypes:

            for i in range(self.pagecount):
                url = self.general_url.format(key=key, pid=i+1)

                items = self.parse_data(url)

                if items:
                    items_all.extend(items)
                else:
                    break

        return items_all

    # 普通
    def parse_data(self, url):

        r = self.get_requests(url)
        r.encoding = 'utf8'

        f = re.search('.*p=(\d+)', url)
        if f:
            page = f.group(1)

        items = []

        try:
            soup = bs(r.text, 'lxml')

            #视频链接-全部结果
            dramaList = soup.find_all('h3')
            for drama in dramaList:

                area_a = drama.find('a')
                if not area_a:
                    continue

                item = DataItem()
                item.title = area_a.text
                item.href = area_a['href']

                try:
                    predrama = drama.parent.parent
                    durationTag = predrama.find('span', attrs={'class':'s_r_time'})
                    if durationTag:
                        item.duration = durationTag.text.strip()
                except Exception,e:
                    print e

                item.page = page
                # try:
                #     item.durationType = self.timelengthDict[int(legth_type)]
                # except Exception,e:
                #     print encode_wrap('未找到对应的时长类型!')

                items.append(item)
        except Exception,e:
            r.lpush(self.redis_video_key, url)
            print 'fun: parse data, ', e

        return items

if __name__=='__main__':
    #key = raw_input('输入搜索关键字:')

    data = pd.read_excel('keys.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
    print data

    video = IFengVideo()
    video.run(data['key'].get_values()[:100])

    #key = '快乐大本营'
    #key = urllib.quote(key.decode(sys.stdin.encoding).encode('gbk'))


