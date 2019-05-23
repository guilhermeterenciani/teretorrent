#!/usr/bin/python3
# -*- coding: utf-8 -*-

#exemplo de: https://stackoverflow.com/questions/22791760/pyqt-adding-rows-to-qtableview-using-qabstracttablemodel

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QAction
from MyTableModel import MyTableModel
import time
from TableModelUpdater import TableModelUpdater

class Ui_MainWindow(object):

    header = ['Arquivo', 'Local' ]
    tableData = [['teste.mp3', 'localhost'], ['teste 2.mp3', '192.168.0.10']]

    def __init__(self, torrent):
        self.torrent = torrent

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

        self. retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        

        self.createTableView()
        self.btnTocar.clicked.connect(self.playSong)

        #self.tableData = self.torrent.listaarquivos
        self.thread = TableModelUpdater(self.torrent) 

        self.thread.threadUpdate.connect(self.threadUpdate)

        self.thread.start()

    def createTableView(self):
        self.tv = self.listaArquivos

        self.tv.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.tableModel = MyTableModel(self.tableData, self.header, self.centralwidget)
        self.tv.setModel(self.tableModel)

        hh = self.tv.horizontalHeader()
        hh.setStretchLastSection(True)

        self.tv.resizeColumnsToContents()
        self.tv.selectRow(0)

    def threadUpdate(self):

        oldId = self.tv.selectionModel().selectedRows()[0].row()

        self.tableModel = MyTableModel(self.thread.items, self.header, self.centralwidget)
        self.tv.setModel(self.tableModel)

        self.tableData = self.thread.items

        try:
            #print(oldId)
            self.tv.selectRow(oldId)
        except:
            print("Oops!" + sys.exc_info()[0] + "occured.")
            print("provavelmente indice %d inválido " % (oldId))

        #print("aeeeeho")

    def playSong(self):
        print( "arquivo solicitado:  " )
        id = self.tv.selectionModel().selectedRows()[0].row()
        print( "índice %d nome %s" %(id, self.tableData[id][0]) )
        
        self.torrent.requisicaodeArquivo(self.tableData[id][0])
        
        self.statusbar.showMessage(self.tableData[id][0] + " solicitado")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TerêTorrent player"))
        self.btnTocar.setText(_translate("MainWindow", "Reproduzir"))

    


if __name__ == "__main__":
    import sys
    
    sys.path.append("../../")
    from torrent import Torrent

    tor = Torrent()

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(tor)
    ui.setupUi(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())
