from PyQt5.QtCore import (QCoreApplication, QObject, QRunnable, QThread,
                          QThreadPool, pyqtSignal)
import time
from MyTableModel import MyTableModel

class TableModelUpdater(QThread):

    threadUpdate = pyqtSignal()

    def __init__(self, torrent ):
        QThread.__init__(self)

        self.items = []
        self.torrent = torrent

    def run(self):
        
        while True:
            for key,val in self.torrent.listaarquivos.items():
                ips = ",".join(val)
                self.items.append([key, ips])

            #self.items = [["aaaaa", "inferno"]]
            self.threadUpdate.emit()
        
            time.sleep(3)

