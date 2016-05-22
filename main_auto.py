#coding: utf-8

import pandas as pd
from videos.video_base import engine_sql, BaseVideo
from videos.VideoFactory import VideoFactory
from util.code_convert import GetNowTime

def run_task():

    table = 'pl_monitor_tasks'
    sql = "select * from {} where status=0".format(table)
    df = pd.read_sql(sql, engine_sql)

    for ix, row in df.iterrows():
        print row

        # 更新任务状态
        sql = 'update {0} set start_date="{1}",lastrun_date="{1}", status={2}'.format(table, GetNowTime(), 1)
        engine_sql.execute(sql)


        task_id = row['id']
        keys = row['keyword'].replace('，',',').split(',')
        platforms = row['monitor_platforms'].replace('，',',').split(',')

        keys = [key.strip() for key in keys]
        platforms = [platform.strip() for platform in platforms]

        for platform in platforms:
            video = VideoFactory.CreateVideo(platform)
            video.task_id = task_id
            video.run_keys(keys, True)

        # 更新任务状态
        sql = 'update {0} set lastrun_date="{1}", status={2}'.format(table, GetNowTime(), 2)
        engine_sql.execute(sql)

if __name__ == "__main__":
    run_task()