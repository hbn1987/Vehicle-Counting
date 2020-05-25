# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created: Fri Feb 28 23:50:30 2020
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(369, 331)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 20, 341, 81))
        self.groupBox.setObjectName("groupBox")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(100, 20, 151, 51))
        self.pushButton.setObjectName("pushButton")
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 110, 341, 211))
        self.groupBox_2.setObjectName("groupBox_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_2.setGeometry(QtCore.QRect(100, 140, 151, 51))
        self.pushButton_2.setObjectName("pushButton_2")
        self.dateEdit_5 = QtWidgets.QDateEdit(self.groupBox_2)
        self.dateEdit_5.setGeometry(QtCore.QRect(150, 41, 110, 31))
        self.dateEdit_5.setDate(QtCore.QDate(2020, 1, 1))
        self.dateEdit_5.setObjectName("dateEdit_5")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(80, 44, 72, 31))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(80, 83, 72, 41))
        self.label_4.setObjectName("label_4")
        self.dateEdit_6 = QtWidgets.QDateEdit(self.groupBox_2)
        self.dateEdit_6.setGeometry(QtCore.QRect(150, 90, 110, 31))
        self.dateEdit_6.setDate(QtCore.QDate(2020, 1, 1))
        self.dateEdit_6.setObjectName("dateEdit_6")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "屏幕船只计数插件"))
        self.groupBox.setTitle(_translate("Dialog", "船只计数"))
        self.pushButton.setText(_translate("Dialog", "开始计数"))
        self.groupBox_2.setTitle(_translate("Dialog", "船只查询"))
        self.pushButton_2.setText(_translate("Dialog", "查询输出"))
        self.dateEdit_5.setDisplayFormat(_translate("Dialog", "yyyy.MM.dd"))
        self.label_3.setText(_translate("Dialog", "开始日期"))
        self.label_4.setText(_translate("Dialog", "结束日期"))
        self.dateEdit_6.setDisplayFormat(_translate("Dialog", "yyyy.MM.dd"))

