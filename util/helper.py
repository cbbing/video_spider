#!/usr/local/bin/python
#coding=utf-8

__author__ = 'bbchen'

import time
from functools import wraps
import pandas as pd
from sqlalchemy import create_engine
import wrapcache

# 统计函数耗时
def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print ("Total time running %s: %s seconds" %
               (function.func_name, str(t1-t0))
               )
        return result
    return function_timer

# 统计函数耗时
def fn_date(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        print '{}() begin run at:{}'.format(function.func_name, time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))
        result = function(*args, **kwargs)
        print '{}() end run at:{}'.format(function.func_name, time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))
        return result
    return function_timer