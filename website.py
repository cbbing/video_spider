__author__ = 'cbb'

# -*- coding: utf-8 -*-
#!/usr/bin/env python

import web
import os

from main import main

from datetime import datetime; now = datetime.now()



urls = (
    '/', 'hello',
    '/download', 'download'
)

app = web.application(urls, globals())

class hello:
    def GET(self, name):
        if not name:
            name = 'World'
        main()
        return 'Hello, ' + name + '!'


BUF_SIZE = 262144

class download:
    def GET(self):
        file_name = 'qq_video.xlsx'
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

if __name__ == "__main__":
    app.run()