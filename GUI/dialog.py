# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import urllib, urllib2
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import pandas as pd
from init import *



class MyTable(QTableWidget):
    def __init__(self,parent=None):
        super(MyTable,self).__init__(parent)

        columns_db = ["Title", "Href", "Duration", "DurationType", "Page", "Time", "Engine", "Source", "KeyMatch", "VideoKey"]
        columns_title = ["标题", "链接", "时长", "时长类型", "页码", "时间", "搜索引擎", "来源", "匹配度", "关键词"]
        columns_zip = zip(range(len(columns_db)), columns_db, columns_title)

        self.setColumnCount(len(columns_db))
        self.setRowCount(10)

        [self.setItem(0,ix,QTableWidgetItem(self.tr(title))) for ix, _, title in columns_zip]

        columns = ["Title", "Href", "Duration", "DurationType", "Page", "Time", "Engine", "Source", "KeyMatch", "VideoKey"]
        sql = "select %s from %s limit 20" % (",".join(columns), mysql_result_table)

        from video_base import engine_sql
        df = pd.read_sql_query(sql, engine_sql)

        self.setRowCount(len(df))

        for ix, row in df.iterrows():
            try:
                [self.setItem(ix+1, index_col, QTableWidgetItem(self.tr(str(row[col])))) for index_col, col, _ in columns_zip]

            except Exception, e:
                print ix, row, str(e)




class LayoutDialog(QDialog):
    def __init__(self, parent=None):
        super(LayoutDialog, self).__init__(parent)
        self.setWindowTitle(self.tr('视频搜索'))

        headerLayout = QHBoxLayout()

        myqq=MyTable()
        myqq.resize(1000, 500)
        myqq.setWindowTitle("My Table")

        label1 = QLabel(self.tr("视频搜索"))
        headerLayout.addWidget(myqq)

        btn_key = QPushButton(self.tr("关键词"))
        btn_run = QPushButton(self.tr("运行"))
        btn_result = QPushButton(self.tr("查看结果"))

        #btn_key.resize(200,200)
        #btn_key.setGeometry(QRect(QPoint(0,0),QSize(200,100)))
        #btn_run.setGeometry(QRect(QPoint(0,0),QSize(200,100)))
        #btn_result.setGeometry(QRect(QPoint(0,0),QSize(200,100)))
        #m_button->setGeometry(QRect(QPoint(100, 100),
         #                        QSize(200, 50)));

        btnLayout = QHBoxLayout()
        btnLayout.addStretch()
        btnLayout.addWidget(btn_key)
        btnLayout.addWidget(btn_run)
        btnLayout.addWidget(btn_result)

        mainLayout = QGridLayout(self)
        mainLayout.setMargin(5)
        mainLayout.setSpacing(10)
        mainLayout.addLayout(headerLayout, 0, 0)
        mainLayout.addLayout(btnLayout, 1, 0)

        self.connect(btn_key, SIGNAL("clicked()"),self.on_openfile_clicked)


    def on_openfile_clicked(self):

        dlg = QFileDialog(self)
        self.filename = dlg.getOpenFileName()
        from os.path import isfile
        if isfile(self.filename):

            # 在 urllib2 上注册 http 流处理句柄
            register_openers()

            # 开始对文件 "DSC0001.jpg" 的 multiart/form-data 编码
            # "image1" 是参数的名字，一般通过 HTML 中的 <input> 标签的 name 参数设置

            # headers 包含必须的 Content-Type 和 Content-Length
            # datagen 是一个生成器对象，返回编码过后的参数
            datagen, headers = multipart_encode({"myfile": open(str(self.filename), "rb")})

            # 创建请求对象
            request = urllib2.Request("http://0.0.0.0:8080/upload", datagen, headers)
            # 实际执行请求并取得返回
            print urllib2.urlopen(request).read()



if __name__ == "__main__":



    app=QApplication(sys.argv)

    dlg = LayoutDialog()
    dlg.resize(1000, 500)
    dlg.show()

    # myqq=MyTable()
    # myqq.resize(600, 300)
    # myqq.setWindowTitle("My Table")
    # myqq.show()

    #Title
    # layout = QHBoxLayout()
    # titleView = QLabel('')
    #
    # btn_import = QPushButton("Keys")
    # btn_run  = QPushButton("Run")
    # btn_result = QPushButton("Result")
    #
    # btn_import.resize(60,30)
    # btn_run.resize(60,30)
    # btn_result.resize(60,30)
    #b.show()


    # layout = QGridLayout()
    # layout.addWidget(btn_import, 0, 0)
    # layout.addWidget(btn_run, 0, 1)
    # layout.addWidget(btn_result, 1, 0)
    #
    # dlg = QDialog()
    # dlg.resize(450,300)
    # dlg.setLayout(layout)
    # dlg.show()
    #
    # app.connect(btn_import, SIGNAL("clicked()"), app, SLOT("quit()"))

    fileName2, ok2 = QFileDialog.getSaveFileName(app,
                                    "文件保存",
                                    "C:/",
                                    "All Files (*);;Text Files (*.txt)")

    app.exec_()
