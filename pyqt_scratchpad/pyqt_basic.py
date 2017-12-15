import PyQt5
import Adddlg
from PyQt5 import QtGui, QtCore, Qt
import download_factory
#cannot change Table Header Color with Windows default style


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTableWidget, QStatusBar, QProgressBar, QTableWidgetItem, QStyleFactory, QVBoxLayout, QMainWindow, QPushButton
from PyQt5.QtGui import QFont, QBrush, QColor
from PyQt5.QtWidgets import QMenuBar, QAction
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QObject
from PyQt5.QtCore import *
from DownloadManager import *
import humanfriendly
header =['Name', 'Status', 'Progress', 'Priority']
header_size = [120,60,170, 60]



class Gui (QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.makeMenuBar()
        self.makeLayout()
        self.makeTable()
        self.makeStatus()
        self.resize(450, 200)
        self.move(300, 300)
        self.setWindowTitle('Simple')
        self.timer = QTimer()
        self.dl_manager = DownloadManager()
        self.timer.timeout.connect(self.refresh)
        self.timer.start(1000)

        self.show()

    #called after makeLayout
    def makeTable(self):
        self.table = QTableWidget(3,4)
        for column in range(len(header)):
            table_item = QTableWidgetItem(header[column])
            header_font = QFont()
            header_font.setBold(True)
            table_item.setFont(header_font)
            self.table.setHorizontalHeaderItem(column, table_item)
            self.table.setColumnWidth(column, header_size[column])
        self.layout.addWidget(self.table, QtCore.Qt.AlignTop)
        self.setCentralWidget(self.table)
        pass

    def add_dl(self):
        to_add = Adddlg.AddDlg()
        #self.to_add.setWindowModality(QtCore.Qt.WindowModal)
        to_add.exec_()
        self.dl_manager.add_download(to_add.url, to_add.target)


    def makeMenuBar(self):
        addAction = QAction('&Add', self)
        addAction.triggered.connect(self.add_dl)
        self.menu = self.menuBar()
        file_menu = self.menu.addMenu('&File')
        self.menu.addMenu('&Downloads')
        self.menu.addMenu('&About')
        file_menu.addAction(addAction)
        pass

    def addAction(self):
        to_add = Adddlg.AddDlg()
        pass

    def makeToolBar(self):
        pass
    def makeButtons(self):
        self.add_btn = QPushButton(self, text="add")
        pass

    def makeLayout(self):
        self.widget = QWidget()
        self.layout = QVBoxLayout()
        #self.layout.addStretch(1)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.layout)



    def makeStatus(self):
        self.status_bar = self.statusBar()

        self.status_bar.showMessage("Status Bar")
        self.status_bar.setFixedHeight(20)
        #self.layout.addWidget(self.status_bar, QtCore.Qt.AlignBottom)

    def addButton(self):
        print("made it here")

    def refresh(self):
        a = 0
        for i in self.dl_manager.gen_list():
            try:
                percent = float(i[1])/float(i[2])
                percent = int(percent *100)
                percent = "%3d%" % (percent, )
                print(percent)
            except:
                percent = 0
            self.table.setItem(a, 0, QTableWidgetItem(i[0]))
            self.table.setItem(a, 1, QTableWidgetItem(str(percent)))
            self.table.setItem(a, 2, QTableWidgetItem(humanfriendly.format_size(int(i[2]))))
            a = a +1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = Gui()
    app.exec_()
    m.dl_manager.stop_all()
    sys.exit(0)

