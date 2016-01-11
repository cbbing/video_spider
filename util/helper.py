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

@wrapcache.wrapcache(timeout=60*60*8)  # 缓存8小时
def get_ip_dataframe():

    host_mysql = 'rdsw5ilfm0dpf8lee609.mysql.rds.aliyuncs.com'
    port_mysql = '3306'
    user_mysql = 'licj'
    pwd_mysql = 'AAaa1234'
    db_name_mysql = 'wealth_db'

    engine = create_engine('mysql+mysqldb://%s:%s@%s:%s/%s' % (user_mysql, pwd_mysql, host_mysql, port_mysql, db_name_mysql), connect_args={'charset':'utf8'})


    mysql_table_ip = 'ip_proxy'
    sql = 'select * from {0} where Speed > 0 order by Speed limit {1}'.format(mysql_table_ip, 1000)
    df_ip = pd.read_sql_query(sql, engine)
    return df_ip