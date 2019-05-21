from PyQt5.QtCore import (QCoreApplication, QObject, QRunnable, QThread,
                          QThreadPool, pyqtSignal)
import time
from MyTableModel import MyTableModel

class TableModelUpdater(QThread):

    threadUpdate = pyqtSignal()

    def __init__(self, torrent ):
        QThread.__init__(self)

        self.torrent = torrent

    def run(self):
        
        while True:
            self.items = []
            for key,val in self.torrent.listaarquivos.items():
                name = key.split("/")
                ips = ",".join(val)
                self.items.append([name[-1], ips])

            #self.items = [["aaaaa", "inferno"]]
            self.threadUpdate.emit()
        
            time.sleep(3)

