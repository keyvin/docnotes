import PyQt5

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QLineEdit, QLabel, QFormLayout, QPushButton, QApplication




class AddDlg(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.success = False
        self.url = ''
        self.target = ''
        self.makeWindow()
        #self.setWindowModality(QtCore.Qt.WindowModal)
        self.exec_()

    def makeWindow(self):
        self.layout = QFormLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(QLabel("URL"))
        self.url_entry = QLineEdit()
        self.layout.addWidget(self.url_entry)
        self.layout.addWidget(QLabel("Destination"))
        self.destination_entry = QLineEdit()
        self.layout.addWidget(self.destination_entry)
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.addClick)
        self.layout.addWidget(self.add_button)
        self.cancel_button = QPushButton("Cancel")
        self.layout.addWidget(self.cancel_button)
        self.cancel_button.clicked.connect(self.cancelClick)
        pass

    def addClick(self):
        #Check that destination is writeable
        #check URL exists
#        print("here")
        self.url = self.url_entry.text()
        self.target = self.destination_entry.text()

        self.destroy()
        if __name__=="__main__":
            sys.exit(0)

    def cancelClick(self):
        print("Cancel")
        pass

if __name__=="__main__":
    app = QApplication([""])
    m=AddDlg()
    app.exec_()