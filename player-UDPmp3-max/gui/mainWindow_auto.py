#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAbstractItemView
from MyTableModel import MyTableModel

class Ui_MainWindow(object):

    header = ['Arquivo', 'Local' ]
    tableData = [['teste.mp3', 'localhost'], ['teste 2.mp3', '192.168.0.10']]

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(588, 372)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listaArquivos = QtWidgets.QTableView(self.centralwidget)
        self.listaArquivos.setObjectName("listaArquivos")
        self.verticalLayout.addWidget(self.listaArquivos)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget_2 = QtWidgets.QWidget(self.widget)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout.addWidget(self.widget_2)
        self.btnTocar = QtWidgets.QPushButton(self.widget)
        self.btnTocar.setObjectName("btnTocar")
        self.horizontalLayout.addWidget(self.btnTocar)
        self.verticalLayout.addWidget(self.widget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 588, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.createTableView()
        self.btnTocar.clicked.connect(self.playSong)

    def createTableView(self):
        self.tv = self.listaArquivos

        self.tv.setSelectionBehavior(QAbstractItemView.SelectRows)

        tableModel = MyTableModel(self.tableData, self.header, self.centralwidget)
        self.tv.setModel(tableModel)

        hh = self.tv.horizontalHeader()
        hh.setStretchLastSection(True)

        self.tv.resizeColumnsToContents()
        self.tv.selectRow(0)

    def playSong(self):
        print( "arquivo solicitado:  " )
        id = self.tv.selectionModel().selectedRows()[0].row()
        print( "índice %d nome %s" %(id, self.tableData[id][0]) )

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TerêTorrent viewer"))
        self.btnTocar.setText(_translate("MainWindow", "Reproduzir"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
