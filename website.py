# -*- coding: utf-8 -*-

#!/usr/bin/env python

__author__ = 'cbb'

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import web
import os, time, hashlib
from main import run_all, run_auto
from util.code_convert import GetTime
from init import *
from video_baidu_no_js import run_baidu

import sys, logging
#from wsgilog import WsgiLog
import ConfigParser

from datetime import datetime; now = datetime.now()
from web import form

db = web.database(dbn='mysql', user='root', pw='root', db='awesome')
render = web.template.render("./www/templates")

urls = (
    '/', 'index',
    '/menu', 'Menu',
    '/download', 'download',
    '/upload', 'Upload',
    '/result', 'resultList',
    '/run_video_search/param=(.*)', 'run_video_search',
    '/run_baidu_search', 'run_baidu_search'

)

app = web.application(urls, globals())

login = form.Form(
    form.Textbox('username'),
    form.Password('password'),
    form.Button('Login'),

    validators = [form.Validator("UserName o r Passwords can't null.", lambda i: len(i.password) > 0 and len(i.username) > 0)]

)

class index:

    def GET(self):

        try:

            cookies = web.cookies().get('videosite')
            cookies = '1234'
            if not cookies == None:
                web.seeother('/menu')
                return
        except Exception, e:
            print str(e)

        f = login()
        return render.formtest(f)

    def POST(self):
        f = login()
        if not f.validates():
            return render.formtest(f)
        else:
            users = db.query("select * from users where name='%s' and password='%s'" % (f.username.value, f.password.value))
            # for user in users:
            #     print user.id, user.name
            if len(users) > 0:
                expires = int(time.time() + 86400)
                web.setcookie('videosite', hashlib.md5('%s-%s-%s' % (f.username.value, f.password.value, str(expires))).hexdigest(), 86400)
                web.seeother('/menu')

class Menu:

    def GET(self):
        return """<html><head>video menu</head><body>
                <li>
                <a target="_self" href="/upload">upload key</a>
                </li>
                <li>
                <a target="_self" href="/run_video_search">run video search</a>
                </li>
                <li>
                <a target="_self" href="/result">result list</a>
                </li>
                </body></html>"""

# class Index:
#     def GET(self):
#         cookies = web.cookies().get('videosite')
#         if cookies == None:
#             web.seeother('/')
#             return
#
#         return """<html><head>videosearch</head><body>
#                 <li>
#                 <a target="_self" href="/upload">upload</a>
#                 </li>
#                 <li>
#                 <a target="_self" href="/run_video_search">run video search</a>
#                 </li>
#                 <li>
#                 <a target="_self" href="/result">result list</a>
#                 </li>
#                 </body></html>"""


class run_video_search:
    def GET(self, param):
        if len(param) > 0:
            run_auto(param)
        return 'Hello, ' + 'Video' + '!'


class run_baidu_search:
    def GET(self):
        run_baidu()
        return 'Hello, ' + 'Video' + '!'



BUF_SIZE = 262144

class download:
    def GET(self, file_name):
        cookies = web.cookies().get('videosite')
        if cookies == None:
            web.seeother('/')
            return

        #file_name = 'qq_video.xlsx'
        file_path = os.path.join('./data', file_name)
        f = None
        try:
            f = open(file_path, "rb")
            web.header('Content-Type','application/octet-stream')
            web.header('Content-disposition', 'attachment; filename=%s' % file_name)
            while True:
                c = f.read(BUF_SIZE)
                if c:
                    yield c
                else:
                    break
        except Exception, e:
            print e
            yield 'Error'
        finally:
            if f:
                f.close()

class Upload:
    def GET(self):
        return """<html><head></head><body>
                <form method="POST" enctype="multipart/form-data" action="">
                <input type="file" name="myfile" />
                <br/>
                <input type="submit" />
                </form>
                </body></html>"""

    def POST(self):

        x = web.input(myfile={})
        print x.myfile
        filedir = www_path # change this to the directory you want to store the file in.
        if 'myfile' in x: # to check if the file-object is created
            filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
            filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
            fout = open(filedir +'/'+ filename,'w') # creates the file where the uploaded file should be stored
            fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
            fout.close() # closes the file, upload complete.

        print type(x)
        print x
        web.debug(x['myfile'].filename)
        web.debug(x['myfile'].value)
        web.debug(x['myfile'].file.read())
        raise web.seeother('/')

class resultList:

    def GET(self):
        #获取文件列表
        files = os.listdir('./data')
        files = [f for f in files if '.xlsx' in f]

        posts = []
        for f in files:
            statinfo = os.stat('./data/%s' % f)
            item = FileItem()
            item.file_name = f
            item.modify_time = GetTime(statinfo.st_ctime)
            posts.append(item)

        return render.list(posts)
        # template = "$def with (infos)\nHello $name"


        template = '''$def with(rows)

        $for row in rows:
            <li>
                <a href="/data/$row.file_name">$row.file_name  $row.modify_time</a>

            </li>
        '''
        hello = web.template.Template(template)
        return hello(posts)

class FileItem:
    def __init__(self):
        self.file_name = ''
        self.modify_time = ''

# class MyLog(WsgiLog):
#     def __init__(self, application):
#
#         cf = ConfigParser.ConfigParser()
#         cf.read('config.ini')
#
#         WsgiLog.__init__(
#             self,
#             application,
#             logformat = "[%(asctime)s] %(filename)s:%(lineno)d(%(funcName)s): [%(levelname)s] %(message)s",
#             tofile = True,
#             toprint = True,
#             file = cf.get("weblog", "file"),
#             interval = cf.get("weblog", "interval"),
#             backups = int(cf.get("weblog", "backups"))
#             )

if __name__ == "__main__":
    app.run()