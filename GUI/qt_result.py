# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'py_result.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import platform
if platform.system() == 'Windows':
    sys.path.append('C:/Code/video_spider')
else:
    sys.path.append('/Users/cbb/Documents/pythonspace/stock-master/')

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import pandas as pd
from sqlalchemy import create_engine
import MySQLdb
#from init import *

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))

from MyLogger import Logger
#from util.code_convert import *


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

class Ui_Result_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(1015, 687)
        self.tableWidget = QtGui.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(20, 90, 981, 541))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setFrameShape(QtGui.QFrame.NoFrame)
        self.tableWidget.setFrameShadow(QtGui.QFrame.Plain)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.pushButton_query = QtGui.QPushButton(Dialog)
        self.pushButton_query.setGeometry(QtCore.QRect(890, 10, 111, 71))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.pushButton_query.setFont(font)
        self.pushButton_query.setObjectName(_fromUtf8("pushButton_query"))
        self.gridLayoutWidget_2 = QtGui.QWidget(Dialog)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(20, 0, 861, 81))
        self.gridLayoutWidget_2.setObjectName(_fromUtf8("gridLayoutWidget_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_9 = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label_9.setFrameShape(QtGui.QFrame.Box)
        self.label_9.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.verticalLayout.addWidget(self.label_9)
        self.dateTimeEdit_end = QtGui.QDateTimeEdit(self.gridLayoutWidget_2)
        self.dateTimeEdit_end.setAlignment(QtCore.Qt.AlignCenter)
        self.dateTimeEdit_end.setObjectName(_fromUtf8("dateTimeEdit_end"))
        self.verticalLayout.addWidget(self.dateTimeEdit_end)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 4, 1, 1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_8 = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label_8.setFrameShape(QtGui.QFrame.Box)
        self.label_8.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.verticalLayout_2.addWidget(self.label_8)
        self.dateTimeEdit_start = QtGui.QDateTimeEdit(self.gridLayoutWidget_2)
        self.dateTimeEdit_start.setAlignment(QtCore.Qt.AlignCenter)
        self.dateTimeEdit_start.setObjectName(_fromUtf8("dateTimeEdit_start"))
        self.verticalLayout_2.addWidget(self.dateTimeEdit_start)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 3, 1, 1)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.label_6 = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label_6.setFrameShape(QtGui.QFrame.Box)
        self.label_6.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.verticalLayout_4.addWidget(self.label_6)
        self.comboBox_source = QtGui.QComboBox(self.gridLayoutWidget_2)
        self.comboBox_source.setObjectName(_fromUtf8("comboBox_source"))
        self.verticalLayout_4.addWidget(self.comboBox_source)
        self.gridLayout_2.addLayout(self.verticalLayout_4, 0, 1, 1, 1)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label_7 = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label_7.setFrameShape(QtGui.QFrame.Box)
        self.label_7.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.verticalLayout_3.addWidget(self.label_7)
        self.comboBox_match = QtGui.QComboBox(self.gridLayoutWidget_2)
        self.comboBox_match.setObjectName(_fromUtf8("comboBox_match"))
        self.verticalLayout_3.addWidget(self.comboBox_match)
        self.gridLayout_2.addLayout(self.verticalLayout_3, 0, 2, 1, 1)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label_3.setFrameShape(QtGui.QFrame.Box)
        self.label_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_5.addWidget(self.label_3)
        self.lineEdit_key = QtGui.QLineEdit(self.gridLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_key.sizePolicy().hasHeightForWidth())
        self.lineEdit_key.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lineEdit_key.setFont(font)
        self.lineEdit_key.setObjectName(_fromUtf8("lineEdit_key"))
        self.verticalLayout_5.addWidget(self.lineEdit_key)
        self.gridLayout_2.addLayout(self.verticalLayout_5, 0, 0, 1, 1)
        self.horizontalLayoutWidget = QtGui.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(760, 639, 241, 32))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        #self.pushButton_pre = QtGui.QPushButton(self.horizontalLayoutWidget)
        #self.pushButton_pre.setObjectName(_fromUtf8("pushButton_pre"))

        #self.horizontalLayout.addWidget(self.pushButton_pre)
        #self.pushButton_next = QtGui.QPushButton(self.horizontalLayoutWidget)
        #self.pushButton_next.setObjectName(_fromUtf8("pushButton_next"))
        #self.horizontalLayout.addWidget(self.pushButton_next)
        self.pushButton_export = QtGui.QPushButton(Dialog)
        self.pushButton_export.setGeometry(QtCore.QRect(10, 640, 114, 32))
        self.pushButton_export.setObjectName(_fromUtf8("pushButton_export"))

        self.condition_init()

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton_query, QtCore.SIGNAL(_fromUtf8("clicked()")), self.table_query)
        #QtCore.QObject.connect(self.pushButton_pre, QtCore.SIGNAL(_fromUtf8("clicked()")), self.tableWidget.show)
        #QtCore.QObject.connect(self.pushButton_next, QtCore.SIGNAL(_fromUtf8("clicked()")), self.tableWidget.reset)
        QtCore.QObject.connect(self.pushButton_export, QtCore.SIGNAL(_fromUtf8("clicked()")), self.data_export)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "视频搜索 - 结果查询", None))
        self.tableWidget.setSortingEnabled(True)
        self.pushButton_query.setText(_translate("Dialog", "查询", None))
        self.label_9.setText(_translate("Dialog", "结束时间", None))
        self.label_8.setText(_translate("Dialog", "开始时间", None))
        self.label_6.setText(_translate("Dialog", "搜索引擎", None))
        self.label_7.setText(_translate("Dialog", "匹配度", None))
        self.label_3.setText(_translate("Dialog", "关键词", None))
        #self.pushButton_pre.setText(_translate("Dialog", "上一页", None))
        #self.pushButton_next.setText(_translate("Dialog", "下一页", None))
        self.pushButton_export.setText(_translate("Dialog", "导出", None))

    def condition_init(self):
        #来源
        source_list = ["不限","百度", "优酷", "土豆", "爱奇艺", "腾讯", "新浪", "搜狐", "乐视", "响巢看看", "华数", "风行", "暴风影音",
                       "PPTV", "56", "酷6","爆米花", "TV189",'央视网', '芒果TV','网易','pipi', '糖豆','哗哩哗哩','acfun','新蓝网',
                       '凤凰视频','音悦台'
                       ]
        source_list_tr = [_translate("Dialog", x, None) for x in source_list]
        self.comboBox_source.addItems(source_list_tr)

        #匹配度
        source_list = ["不限","完全匹配", "模糊匹配", "不匹配"]
        source_list_tr = [_translate("Dialog", x, None) for x in source_list]
        self.comboBox_match.addItems(source_list_tr)

        #时间
        nowTime = QDateTime.currentDateTime()
        startTime = QTime.fromString("00:00", "HH:mm")
        nowTime.setTime(startTime)
        self.dateTimeEdit_start.setDateTime(nowTime)
        self.dateTimeEdit_start.setDisplayFormat("yyyy-MM-dd HH:mm")
        self.dateTimeEdit_start.setCalendarPopup(True)

        endTime = QTime.fromString("23:59", "HH:mm")
        nowTime.setTime(endTime)
        #nowTime = nowTime.addDays(1)
        self.dateTimeEdit_end.setDateTime(nowTime)
        self.dateTimeEdit_end.setDisplayFormat("yyyy-MM-dd HH:mm")
        self.dateTimeEdit_end.setCalendarPopup(True)

        self.df = pd.DataFrame()

        self.infoLogger = Logger(logname='info_ui.log', logger='I')
        self.errorLogger = Logger(logname='error_ui.log', logger='E')


    def table_query(self):
        columns_db = ["Title", "Href", "Duration", "DurationType", "Page", "Time", "Engine", "Source", "KeyMatch", "VideoKey"]
        columns_title = ["标题", "链接", "时长", "时长类型", "页码", "时间", "搜索引擎", "来源", "匹配度", "关键词"]
        columns_zip = zip(range(len(columns_db)), columns_db, columns_title)

        self.tableWidget.setColumnCount(len(columns_db))
        self.tableWidget.setRowCount(1)

        [self.tableWidget.setItem(0,ix,QTableWidgetItem(self.tableWidget.tr(title))) for ix, _, title in columns_zip]

        columns = ["Title", "Href", "Duration", "DurationType", "Page", "Time", "Engine", "Source", "KeyMatch", "VideoKey"]

        sql = "select %s from %s " % (",".join(columns), "video_result")
        #sql = "select * from %s " % ( "video_result")
        #添加条件

        if len(self.lineEdit_key.displayText()) > 0:
            keys = unicode(self.lineEdit_key.displayText().toUtf8(), 'utf-8', 'ignore')
            #kyes = str(keys)

            keys = keys.replace(',', '|')
            keys = keys.replace('，', '|')

            if 'where' in sql:
                sql = sql + "and VideoKey like '%%%s%%' " % keys
            else:
                #sql = sql + "where VideoKey like '%%%s%%' " % keys
                sql = sql + "where VideoKey regexp '%s'" % keys

        currentIndex_source = self.comboBox_source.currentIndex()
        if currentIndex_source != 0:
            if 'where' in sql:

                sql = sql +  "and Engine='%s' " % self.comboBox_source.currentText()
                # if currentIndex_source == 12 or currentIndex_source == 18 or currentIndex_source == 11: #11,风行
                #     sql = sql +  "and Engine='%s' " % self.comboBox_source.currentText()
                # else:
                #     sql = sql +  "and Source='%s' " % self.comboBox_source.currentText()
            else:
                sql = sql +  "where Engine='%s' " % self.comboBox_source.currentText()
                # if currentIndex_source == 12 or currentIndex_source == 18 or currentIndex_source == 11: #11,风行
                #     sql = sql +  "where Engine='%s' " % self.comboBox_source.currentText()
                # else:
                #     sql = sql +  "where Source='%s' " % self.comboBox_source.currentText()

        if self.comboBox_match.currentIndex() != 0:
            if 'where' in sql:
                sql = sql +  "and KeyMatch='%s' " % self.comboBox_match.currentText()
            else:
                sql = sql +  "where KeyMatch='%s' " % self.comboBox_match.currentText()

        date_start_str = self.dateTimeEdit_start.text() + ':00'
        date_end_str = self.dateTimeEdit_end.text() + ':59'
        if 'where' in sql:
            sql = sql + " and Time>'%s' and Time <'%s' " %(date_start_str, date_end_str)
        else:
            sql = sql + " where Time>'%s' and Time <'%s' " %(date_start_str, date_end_str)


        self.infoLogger.logger.info( sql)
        print sql
        #from video_base import engine_sql
        try:
            conn=MySQLdb.connect(host="shipinjiankong.mysql.rds.aliyuncs.com",user="shipin",passwd="AAaa0924",db="shipinjiankong",charset="utf8")
            cur = conn.cursor()
            cur.execute(sql)

            results = cur.fetchall()
            data1 = {columns[0]:[result[0] for result in results],
                    columns[1]:[result[1] for result in results],
                    }
            data = {columns[i]:[result[i] for result in results] for i in range(len(columns))}
            self.df = pd.DataFrame(data, columns=columns)

            self.infoLogger.logger.info('result len:%s' % len(self.df))
            # for result in cur.fetchall():
            #     print result
            #     self.infoLogger.logger.info(str(result))
            #     break
            # self.infoLogger.logger.info('end')
            #
            # engine_sql = create_engine('mysql+mysqldb://shipin:AAaa0924@shipinjiankong.mysql.rds.aliyuncs.com:3306/shipinjiankong',
            #            connect_args={'charset':'utf8'})
            # self.df = pd.read_sql_query(sql, engine_sql)
        except Exception, e:
            self.errorLogger.logger.error(str(e))

        #self.infoLogger.logger.info(encode_wrap(len(self.df)))

        self.tableWidget.setRowCount(len(self.df))

        for ix, row in self.df.iterrows():
            try:
                [self.tableWidget.setItem(ix+1, index_col, QTableWidgetItem(self.tableWidget.tr(str(row[col])))) for index_col, col, _ in columns_zip]

            except Exception, e:
                print ix, row, str(e)

    def data_export(self):



        #按关键词分组
        # dfs = []
        # keys_se = self.df['VideoKey'].drop_duplicates()
        # for video_key in list(keys_se):
        #     df_each = self.df[self.df['VideoKey'] == video_key]
        #     dfs.append((video_key, df_each))

        print self.df.columns
        self.df = self.df.drop_duplicates(['Href'])

        file_name = QFileDialog.getSaveFileName(self.pushButton_export,
                                    self.tableWidget.tr("保存文件"),
                                    "",
                                    "Excel Files (*.xlsx);;CSV (*.csv)")
        print file_name
        if len(file_name) > 0:
            file_name_unicode = str_qt_to_utf(file_name)
            if file_name_unicode.endswith('csv'):
                self.df.to_csv(file_name_unicode, index=True)
            else:
                with pd.ExcelWriter(file_name_unicode) as writer:
                    self.df.to_excel(writer, sheet_name='Sheet1', index=True)
                # for key, df in dfs:
                #     df.to_excel(writer, sheet_name=key)

        #self.infoLogger.logger.info(encode_wrap('写入excel完成'))


def encode_wrap(str):
    try:
        sse = sys.stdout.encoding
        return str.encode(sse)
    except Exception, e:
        return str

def str_qt_to_utf(qt_str):
    utf_str = unicode(qt_str.toUtf8(), 'utf-8', 'ignore')
    return utf_str

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Result_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

