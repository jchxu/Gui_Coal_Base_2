# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'index_trend_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_index_trend_dialog(object):
    def setupUi(self, index_trend_dialog):
        index_trend_dialog.setObjectName("index_trend_dialog")
        index_trend_dialog.resize(1200, 600)
        self.label_3 = QtWidgets.QLabel(index_trend_dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 50, 41, 31))
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label = QtWidgets.QLabel(index_trend_dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 201, 31))
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.comboBox_2 = QtWidgets.QComboBox(index_trend_dialog)
        self.comboBox_2.setGeometry(QtCore.QRect(100, 50, 120, 30))
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(12)
        self.comboBox_2.setFont(font)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.screening_btn = QtWidgets.QPushButton(index_trend_dialog)
        self.screening_btn.setGeometry(QtCore.QRect(250, 40, 170, 50))
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.screening_btn.setFont(font)
        self.screening_btn.setObjectName("screening_btn")

        self.retranslateUi(index_trend_dialog)
        self.screening_btn.clicked.connect(index_trend_dialog.screening_btn_click)
        QtCore.QMetaObject.connectSlotsByName(index_trend_dialog)

    def retranslateUi(self, index_trend_dialog):
        _translate = QtCore.QCoreApplication.translate
        index_trend_dialog.setWindowTitle(_translate("index_trend_dialog", "煤种质量变化趋势"))
        self.label_3.setText(_translate("index_trend_dialog", "煤种"))
        self.label.setText(_translate("index_trend_dialog", "煤种筛选条件"))
        self.comboBox_2.setItemText(0, _translate("index_trend_dialog", "焦煤"))
        self.comboBox_2.setItemText(1, _translate("index_trend_dialog", "肥煤"))
        self.comboBox_2.setItemText(2, _translate("index_trend_dialog", "气煤"))
        self.comboBox_2.setItemText(3, _translate("index_trend_dialog", "1/3焦煤"))
        self.comboBox_2.setItemText(4, _translate("index_trend_dialog", "瘦煤"))
        self.screening_btn.setText(_translate("index_trend_dialog", "绘制质量趋势图"))

