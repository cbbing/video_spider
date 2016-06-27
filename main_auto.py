#coding: utf-8

import pandas as pd
from videos.video_base import engine_sql, BaseVideo
from videos.VideoFactory import VideoFactory
from util.code_convert import GetNowTime
import json
from apscheduler.schedulers.blocking import BlockingScheduler
from util.helper import fn_date
from videos.video_base import AutoItem

@fn_date
def run_task():

    table = 'pl_scrapy_tasks'
    sql = "select * from {} where status=1 and run_time<'{}'".format(table, GetNowTime())
    df = pd.read_sql(sql, engine_sql)
    # print "len:", len(df)

    for ix, row in df.iterrows():
        print row
        task_id = row['id']

        # 更新任务状态 -任务开始
        sql = 'update {0} set started_time="{1}", status=2 where id="{2}"'.format(table, GetNowTime(), task_id)
        engine_sql.execute(sql)

        # 解析关键词与非关键词
        print row['keyword']

        keyword = row['keyword'].replace('NaN', '""')
        df = pd.read_json(keyword)
        print df


        keys = df['key'].get_values()
        platforms = row['monitor_platforms'].replace('，',',').split(',')

        keys = [key.strip() for key in keys]
        platforms = [platform.strip() for platform in platforms if len(platform.strip())>0]

        autoItem = AutoItem()
        autoItem.scrapy_task_id = task_id
        autoItem.monitor_id = row['monitor_task_id']
        autoItem.df_keys = df

        for platform in platforms:
            video = VideoFactory.CreateVideo(platform)
            video.autoItem = autoItem
            # video.scrapy_task_id = task_id
            # video.monitor_task_id = row['monitor_task_id']
            video.run_keys(keys, True)

        # 更新任务状态 - 任务完成
        sql = 'update {0} set finished_time="{1}", status={2} where id="{3}"'.format(table, GetNowTime(), 3, task_id)
        engine_sql.execute(sql)






if __name__ == "__main__":

    run_task()
    exit(0)


    sched = BlockingScheduler()

    # 抓取
    sched.add_job(run_task, 'cron', minute='*/10')  # hour=1,
    sched.start()