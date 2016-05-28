#coding:utf-8

import pandas as pd
from check_404 import check_404_by_requests
import os
from util.code_convert import encode_wrap
import time

def quchong_youku(filename):
    try:
        df = pd.read_excel(filename)
        df['Status'] = '有效'
        for ix, row in df.iterrows():
            df.ix[ix, 'Status'] = '有效' if check_404_by_requests(row['Href']) else '失效'
            status =encode_wrap( '排查:{}/{}'.format(ix+1, len(df)))
            print status
            time.sleep(1)

        df.to_excel(filename.replace('.xlsx','')+'(checked).xlsx', index=False)
        print 'success'
    except Exception,e:
        print 'Error:', e

def run_quchong():
    dir = 'D:\Data\QuChong\\'
    for name in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, name)):
            filename = os.path.join(dir,name)
            print filename
            if name.endswith('.xlsx') and 'checked' not in name:
                quchong_youku(filename)

if __name__ == "__main__":
    run_quchong()