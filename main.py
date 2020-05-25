# -*- coding: utf-8 -*-
import sys
import gui
from PyQt5.QtWidgets import QApplication, QMainWindow
from dbmanipulation import processInit, queryDB
from datetime import datetime
import time
from dateutil import relativedelta
from excelwriter import writeexcl
import os
from imagegrab import imagegrab

class MyMainForm(QMainWindow, gui.Ui_Dialog):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        #添加读取按钮信号和槽，注意display函数不加小括号
        self.pushButton.clicked.connect(self.videocap)
        #添加查询按钮信号和槽
        self.pushButton_2.clicked.connect(self.query)


    def videocap(self):
        imagegrab()

    def query(self):
        resdict=[]
        start = self.dateEdit_5.text()
        end = self.dateEdit_6.text()
        start = datetime(int(start[0:4]), int(start[5:7]), int(start[8:10]))
        end = datetime(int(end[0:4]), int(end[5:7]), int(end[8:10]))
        days = (end - start).days
        #错误输入排除
        if days < 0:
            temp = start
            start = end
            end = start
            days = -days
        elif days == 0:
            days += 1
        interval = 86400
        res = queryDB(start, end)
        if res.count()!=0:
            for re in res:
                resdict.append(re['timeStamp'])
        counterperday = []
        num = 0
        for i in range(days):
            daycounter = [(start+relativedelta.relativedelta(days=i)).strftime("%Y-%m-%d")]
            intervals = [time.mktime(start.timetuple())+interval*i, time.mktime(start.timetuple())+interval*(i+1)]
            for j in resdict:
                if j >= intervals[0] and j < intervals[1]:
                    num += 1
            daycounter.append(num)
            counterperday.append(daycounter)
        writeexcl(counterperday, start.strftime("%Y-%m-%d")+'_'+end.strftime("%Y-%m-%d"))
        fname = 'vessel_report' + start.strftime("%Y-%m-%d")+'_'+end.strftime("%Y-%m-%d") + '.xlsx'
        os.system(fname)



if __name__ == '__main__':
    # 初始化mongodb
    processInit()
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    # 将窗口控件显示在屏幕上
    myWin.show()
    # 程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())
