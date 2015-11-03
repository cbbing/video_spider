# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'py_main.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import urllib, urllib2
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

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

    # 上传文件
    def on_openfile_clicked(self):

        dlg = QFileDialog()
        filename = dlg.getOpenFileName()
        from os.path import isfile
        if isfile(filename):

            # 在 urllib2 上注册 http 流处理句柄
            register_openers()

            # 开始对文件 "DSC0001.jpg" 的 multiart/form-data 编码
            # "image1" 是参数的名字，一般通过 HTML 中的 <input> 标签的 name 参数设置

            # headers 包含必须的 Content-Type 和 Content-Length
            # datagen 是一个生成器对象，返回编码过后的参数
            datagen, headers = multipart_encode({"myfile": open(str(filename), "rb")})

            # 创建请求对象
            request = urllib2.Request("http://0.0.0.0:8080/upload", datagen, headers)
            # 实际执行请求并取得返回
            print urllib2.urlopen(request).read()

    #运行
    def on_run_clicked(self):
        response = urllib.urlopen('http://0.0.0.0:8080/run_video_search')
        print response

    #结果
    def on_show_result(self):
        from dialog import MyTable
        myqq=MyTable()
        myqq.resize(1000, 500)
        myqq.setWindowTitle("My Table")
        myqq.show()
        myqq.exec_()

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

