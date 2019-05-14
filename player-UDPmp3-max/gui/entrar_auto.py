# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'entrar.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(288, 161)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.txtEntrar = QtWidgets.QLineEdit(self.centralwidget)
        self.txtEntrar.setObjectName("txtEntrar")
        self.horizontalLayout.addWidget(self.txtEntrar)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.btnEntrar = QtWidgets.QPushButton(self.centralwidget)
        self.btnEntrar.setObjectName("btnEntrar")
        self.verticalLayout_2.addWidget(self.btnEntrar)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 288, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.txtEntrar.setText("teste")

        self.btnEntrar.clicked.connect(self.enter)

    def enter(self):
        msg = "bem vindo " + self.txtEntrar.text()+ "\nlogging in, wait just a sec."
        print(msg)
        sys.exit()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Entrar"))
        self.label.setText(_translate("MainWindow", "Nome"))
        self.btnEntrar.setText(_translate("MainWindow", "Entrar"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
