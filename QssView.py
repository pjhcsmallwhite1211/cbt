import sys,ui,lib
from PyQt5.QtWidgets import QApplication, QMainWindow,QLabel,QFrame,QHBoxLayout
from PyQt5.QtCore import QTimer
from PyQt5 import QtGui
class UserWindow(object):
    def __init__(self):

        self.app=QApplication(sys.argv)
        self.main=QMainWindow()
        self.ui = ui.Ui_MainWindow()
        self.ui.setupUi(self.main)
        self.main.show()
        self.setStyle()
        self.ui.send.clicked.connect(self.setStyle)
        self.ui.send_2.clicked.connect(self.setStyle)

    def setStyle(self):
        self.main.setStyleSheet(lib.read_qss_file('./css.qss'))
    
    def run(self):
        sys.exit(self.app.exec_())
if __name__ == '__main__':
    user=UserWindow()

    user.run()