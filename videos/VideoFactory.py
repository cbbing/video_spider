#coding: utf-8

from video_youku import YoukuVideo
from video_tudou import TudouVideo
from video_sina import SinaVideo
from video_qq import QQVideo
from video_sohu import SouhuVideo
from video_iqiyi import IQiYiVideo
from video_letv import LetvVideo
from video_huashu import HuashuVideo
from video_fun import FunVideo
#from video_kankan import KankanVideo
from video_kankan_no_js import KanKanVideo
from video_baofeng import BaofengVideo
#from video_baidu import BaiduVideo
from video_pptv import PPTVVideo
from video_56 import V56Video
from video_ku6 import Ku6Video
from video_baomihua import BaomihuaVideo
from video_tv189 import TV189Video
from video_cctv import CCTVVideo
from video_hunantv import HuNanTVVideo
from video_163 import V163Video
from video_pipi import PiPiVideo
from video_tangdou import TangDouVideo
from video_bilibili import BilibiliVideo
from video_acfun import AcFunVideo
from video_weibo import WeiboVideo
from video_cztv import CZTVVideo

class VideoFactory():

    @staticmethod
    def CreateVideo(platform):
        if platform == '优酷':
            return YoukuVideo()
        elif platform == '土豆':
            return TudouVideo()
        elif platform == '新浪视频':
            return SinaVideo()
        elif platform == '搜狐视频':
            return SouhuVideo()
        elif platform == '腾讯视频':
            return QQVideo()
        elif platform == '爱奇艺':
            return IQiYiVideo()
        elif platform == '乐视':
            return LetvVideo()
        elif platform == '华数':
            return HuashuVideo()
        elif platform == '风行':
            return FunVideo()
        elif platform == '响巢看看':
            return KanKanVideo()
        elif platform == '暴风影音':
            return BaofengVideo()
        elif platform == 'PPTV':
            return PPTVVideo()
        elif platform == '56网':
            return V56Video()
        elif platform == '酷6':
            return Ku6Video()
        elif platform == '爆米花':
            return BaomihuaVideo()
        elif platform == 'TV189':
            return TV189Video()
        elif platform == '央视网':
            return CCTVVideo()
        elif platform == '芒果TV':
            return HuNanTVVideo()
        elif platform == '网易视频':
            return V163Video()
        elif platform == 'pipi':
            return PiPiVideo()
        elif platform == '糖豆':
            return TangDouVideo()
        elif platform == '哔哩哔哩':
            return BilibiliVideo()
        elif platform == 'acfun':
            return AcFunVideo()
        elif platform == '新蓝网':
            return CZTVVideo()


if __name__ == "__main__":
    video = VideoFactory.CreateVideo('优酷')

    print type(video)

