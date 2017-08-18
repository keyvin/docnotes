import PyQt5
from PyQt5 import QtGui, QtCore, Qt

#cannot change Table Header Color with Windows default style


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTableWidget, QStatusBar, QProgressBar, QTableWidgetItem, QStyleFactory, QVBoxLayout, QMainWindow
from PyQt5.QtGui import QFont, QBrush, QColor
from PyQt5.QtWidgets import QMenuBar, QAction

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

    def makeMenuBar(self):
        self.menu = self.menuBar()
        self.menu.addMenu('&File')
        self.menu.addMenu('&Downloads')
        self.menu.addMenu('&About')

        pass

    def makeToolBar(self):
        pass
    def makeButtons(self):
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    #to change table properties.
    #app.setStyle(QStyleFactory.create("Fusion"));

    #Paint Brush options
    #brush = QBrush()
    #brush.setColor(QColor(200,200,40))
    m = Gui()


#    progress = QProgressBar()
 #   progress.setValue(85)
#    table = QTableWidget(5,5)
    #to add to bottom. insertat is another option. set layout to begin at top.


    #table.setCellWidget(0, 1, progress )
    #l = QLabel('hello', w)
#    table_item.setBackground(QColor(100,100,150))




    sys.exit(app.exec_())
