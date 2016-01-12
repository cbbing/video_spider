# -*- coding: utf-8 -*-

from util.webHelper import get_requests, get_web_driver
from video_base import engine_sql
import time

def check_404(date_start=None, date_end=None):
    """
    检测是否有无效链接
    :param date_start:
    :param date_end:
    :return:
    """
    url = 'http://v.youku.com/v_show/id_XNjIyMzEwODU2.html?from=s1.8-1-1.2'

    #r = get_requests(url, has_proxy=False)

    # print '\n'
    # print r.url
    # print r.is_redirect

    driver = get_web_driver(url, False)
    print driver.current_url
    time.sleep(20)
    print driver.current_url
    driver.close()

check_404()
