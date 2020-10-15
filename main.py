import sys
import os
import ctypes
import qdarkstyle
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Project.Layouts.MainLayout import MainLayout
from Project.Layouts.SettingsLayout import SettingsLayout

if sys.platform == "win32":
    myAppId = u"jakubmelkowski.pedestriancounter"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppId)


appWidth, appHeight = 1000, 800


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Pedestrian Counter")
        self.setFixedSize(appWidth, appHeight)
        self.settingsLayout = SettingsLayout()

        mainLayout = MainLayout()
        mainLayout.addLayout(self.settingsLayout, 0, 0)

        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainWindow = MainWindow()
    sys.exit(app.exec_())
