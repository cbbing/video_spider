# -*- coding: utf-8 -*-
#!/usr/bin/env python

__author__ = 'cbb'

import platform

systemName = platform.system()

#配置文件 位置
config_file_path = 'config.ini'
if systemName == 'Windows':
    config_file_path = 'C:\Users\Administrator\Desktop\Data\config.ini'

#关键词 - 文件位置
key_path = 'keys.xlsx'
if systemName == 'Windows':
    key_path = 'C:\Users\Administrator\Desktop\Data\keys.xlsx'

#结果目录
if systemName == 'Windows':
    dir_path = 'C:/Users/Administrator/Desktop/Data/Result/'
else:
    dir_path = './data/'