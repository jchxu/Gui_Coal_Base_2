# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mine_info_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_mine_info_dialog(object):
    def setupUi(self, mine_info_dialog):
        mine_info_dialog.setObjectName("mine_info_dialog")
        mine_info_dialog.resize(800, 600)
        self.label = QtWidgets.QLabel(mine_info_dialog)
        self.label.setGeometry(QtCore.QRect(240, 20, 661, 60))
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setOpenExternalLinks(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(mine_info_dialog)
        self.label_2.setGeometry(QtCore.QRect(240, 100, 241, 60))
        self.label_2.setTextFormat(QtCore.Qt.RichText)
        self.label_2.setOpenExternalLinks(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(mine_info_dialog)
        self.label_3.setGeometry(QtCore.QRect(240, 180, 271, 60))
        self.label_3.setTextFormat(QtCore.Qt.RichText)
        self.label_3.setOpenExternalLinks(True)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(mine_info_dialog)
        self.label_4.setGeometry(QtCore.QRect(20, 180, 200, 60))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("中国煤炭市场网logo_03.jpg"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(mine_info_dialog)
        self.label_5.setGeometry(QtCore.QRect(20, 20, 200, 60))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap("国家煤炭工业网logo.jpg"))
        self.label_5.setScaledContents(True)
        self.label_5.setOpenExternalLinks(True)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(mine_info_dialog)
        self.label_6.setGeometry(QtCore.QRect(20, 100, 200, 60))
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap("中国煤炭资源网logo.png"))
        self.label_6.setScaledContents(True)
        self.label_6.setObjectName("label_6")

        self.retranslateUi(mine_info_dialog)
        QtCore.QMetaObject.connectSlotsByName(mine_info_dialog)

    def retranslateUi(self, mine_info_dialog):
        _translate = QtCore.QCoreApplication.translate
        mine_info_dialog.setWindowTitle(_translate("mine_info_dialog", "煤矿/矿山信息"))
        self.label.setText(_translate("mine_info_dialog", "<html><head/><body><p><a href=\"http://www.coalchina.org.cn/\"><span style=\" font-size:14pt; text-decoration: underline; color:#0000ff;\">http://www.coalchina.org.cn/</span></a></p></body></html>"))
        self.label_2.setText(_translate("mine_info_dialog", "<html><head/><body><p><a href=\"http://www.sxcoal.com/\"><span style=\" font-size:14pt; text-decoration: underline; color:#0000ff;\">http://www.sxcoal.com/</span></a></p></body></html>"))
        self.label_3.setText(_translate("mine_info_dialog", "<html><head/><body><p><a href=\"https://www.cctd.com.cn/\"><span style=\" font-size:14pt; text-decoration: underline; color:#0000ff;\">https://www.cctd.com.cn/</span></a></p></body></html>"))

