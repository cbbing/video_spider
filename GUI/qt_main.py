# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'py_main.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui, QtNetwork

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os
import urllib, urllib2
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

from qt_result import Ui_Result_Dialog

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(645, 389)
        self.horizontalLayoutWidget = QtGui.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 10, 571, 80))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(23)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.horizontalLayoutWidget_2 = QtGui.QWidget(Dialog)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(30, 110, 574, 141))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton_key = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_key.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_key.sizePolicy().hasHeightForWidth())
        self.pushButton_key.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton_key.setFont(font)
        self.pushButton_key.setIconSize(QtCore.QSize(80, 80))
        self.pushButton_key.setObjectName(_fromUtf8("pushButton_key"))
        self.horizontalLayout_2.addWidget(self.pushButton_key)
        self.pushButton_run = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_run.sizePolicy().hasHeightForWidth())
        self.pushButton_run.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton_run.setFont(font)
        self.pushButton_run.setObjectName(_fromUtf8("pushButton_run"))
        self.horizontalLayout_2.addWidget(self.pushButton_run)
        self.pushButton_result = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_result.sizePolicy().hasHeightForWidth())
        self.pushButton_result.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton_result.setFont(font)
        self.pushButton_result.setObjectName(_fromUtf8("pushButton_result"))
        self.horizontalLayout_2.addWidget(self.pushButton_result)
        self.horizontalLayoutWidget_3 = QtGui.QWidget(Dialog)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(30, 260, 581, 111))
        self.horizontalLayoutWidget_3.setObjectName(_fromUtf8("horizontalLayoutWidget_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton_key, QtCore.SIGNAL(_fromUtf8("clicked()")), self.on_openfile_clicked)
        QtCore.QObject.connect(self.pushButton_run, QtCore.SIGNAL(_fromUtf8("clicked()")), self.on_run_clicked)
        QtCore.QObject.connect(self.pushButton_result, QtCore.SIGNAL(_fromUtf8("clicked()")), self.on_show_result)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "视频搜索", None))
        self.label.setText(_translate("Dialog", "视频搜索程序", None))
        self.pushButton_key.setText(_translate("Dialog", "关键词", None))
        self.pushButton_run.setText(_translate("Dialog", "运行", None))
        self.pushButton_result.setText(_translate("Dialog", "结果", None))

        self.ip = "101.200.183.216"

    # 上传文件
    def on_openfile_clicked(self):


        dlg = QFileDialog()
        filename = dlg.getOpenFileName()
        from os.path import isfile
        if isfile(filename):
            filename = str(filename)
            print type(filename)
            #dir_f = os.path.dirname(str(filename))

            # ------ web post -----
            # # 在 urllib2 上注册 http 流处理句柄
            # register_openers()
            #
            # # headers 包含必须的 Content-Type 和 Content-Length
            # # datagen 是一个生成器对象，返回编码过后的参数
            # datagen, headers = multipart_encode({"myfile": open(str(filename), "rb")})
            #
            # # 创建请求对象
            # request = urllib2.Request("http://%s:8080/upload" % self.ip, datagen, headers)
            # # 实际执行请求并取得返回
            # print urllib2.urlopen(request).read()


            # ------- ftp --------
            from ftplib import FTP

            ftp=FTP()
            ftp.set_debuglevel(2)#打开调试级别2，显示详细信息;0为关闭调试信息
            ftp.connect('101.200.183.216','21')#连接
            ftp.login('Administrator','AAaa0924')#登录，如果匿名登录则用空串代替即可
            print ftp.getwelcome()#显示ftp服务器欢迎信息
            #ftp.cwd(dir_f) #选择操作目录
            #filename='keys.xlsx'
            bufsize = 1024#设置缓冲块大小
            file_handler = open(filename,'rb')#以读模式在本地打开文件
            ftp.storbinary('STOR %s' % os.path.basename(filename),file_handler,bufsize)#上传文件
            ftp.set_debuglevel(0)
            file_handler.close()
            ftp.quit()
            print "ftp up OK"

            msgBox = QtGui.QMessageBox()
            msgBox.setText(_fromUtf8("上传完毕"))
            #msgBox.setInformativeText("Do you really want to disable safety enforcement?")
            msgBox.addButton(QtGui.QMessageBox.Ok)
            #msgBox.addButton(QtGui.QMessageBox.No)
            #msgBox.setDefaultButton(QtGui.QMessageBox.No)
            msgBox.exec_()





    #运行
    def on_run_clicked(self):
        # btn =  RunButton()
        # btn.show()
        self.pushButton_run.setText(_translate("Dialog", "运行中", None))
        self.pushButton_run.setEnabled(False)
        response = urllib2.urlopen('http://%s:8080/run_video_search' % self.ip, timeout=3)
        print response

        # progress = QtGui.QProgressDialog("running...", "ok", 0, 10)
        # progress.show()
        # t = WorkThread()
        # t.punched.connect(lambda : progress.setValue(progress.value()+1))
        # t.start()


    #结果
    def on_show_result(self):

        Dialog = QtGui.QDialog()
        ui = Ui_Result_Dialog()
        ui.setupUi(Dialog)
        Dialog.show()
        Dialog.exec_()

        # from dialog import MyTable
        # myqq=MyTable()
        # myqq.resize(1000, 500)
        # myqq.setWindowTitle("My Table")
        # myqq.show()
        # myqq.exec_()

class RunButton(QtGui.QPushButton):
    def __init__(self, parent=None):
        super(QPushButton, self).__init__(parent=parent)

        self.ip = "101.200.183.216"

        self.http = QtNetwork.QHttp(parent=self)
        self.http.done.connect(self.on_req_done)

        self.url = QtCore.QUrl('http://%s:8080/result' % self.ip)

        self.http.setHost(self.url.host(), self.url.port(8080))
        self.getId = self.http.get(self.url.path())

    def on_req_done(self, error):
        if not error:
            print "Success!"
        else:
            print "Error!"

class WorkThread(QtCore.QThread):

    punched = QtCore.pyqtSignal()

    def __init__(self):
        QtCore.QThread.__init__(self)

        self.ip = "101.200.183.216"

    def __del__(self):
        self.wait()

    def run(self):
        response = urllib.urlopen('http://%s:8080/run_video_search' % self.ip)
        self.punched.emit()
        self.terminate()

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

