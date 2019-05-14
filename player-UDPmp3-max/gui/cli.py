#!/usr/bin/python3
# coding: utf-8

import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget


app = QApplication(sys.argv)

window = QWidget()
window.setGeometry(50,50,500,300)
window.setWindowTitle("teste")

window.show()

app.exec()