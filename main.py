import sys
import os
import ctypes
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Project.Layouts.MainLayout import MainLayout

if sys.platform == "win32":
    myAppId = u"jakubmelkowski.pedestriancounter"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppId)

app = QApplication(sys.argv)
appWidth, appHeight = 1000, 800


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Pedestrian Counter")
        self.setFixedSize(appWidth, appHeight)

        mainLayout = MainLayout()

        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)
        self.show()


mainWindow = MainWindow()
app.exec_()
