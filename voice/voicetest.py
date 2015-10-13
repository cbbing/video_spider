# -*- coding:utf-8 -*-

__author__ = 'cbb'

import requests
import json

url_token = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=NutboxpmHeUDd2qrWLhULpxC&client_secret=uDKEeZsQWMGmk6TeC3osWFWdgEsgHhxS"

r = requests.get(url_token)
print r.text

#转dict
resultDict = json.loads(r.text)
print type(resultDict)
access_token = resultDict['access_token']