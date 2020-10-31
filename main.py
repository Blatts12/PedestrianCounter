import sys
import os
import ctypes
import qdarkstyle
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Project.Layouts.MainLayout import MainLayout
from Project.Layouts.SettingsLayout import SettingsLayout
from Project.Layouts.DisplayLayout import DisplayLayout
from Project.Layouts.ImageViewerLayout import ImageViewerLayout
from Project.Layouts.InfoLayout import InfoLayout
from Project.Components.OpenCVImageViewer import OpenCVImageViewer
from Project.PedestrianCounter.MainProcess import MainProcessThread
from Project.PedestrianCounter.Detecting import Detectors
from Project.PedestrianCounter.Tracking import TRAKCERS

if sys.platform == "win32":
    myAppId = u"jakubmelkowski.pedestriancounter"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppId)


appWidth, appHeight = 1000, 800
windowName = "Pedestrian Counter"


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle(windowName)
        self.setFixedSize(appWidth, appHeight)
        self.settingsLayout = SettingsLayout()
        self.displayLayout = DisplayLayout()
        self.mainProcessThread = MainProcessThread()

        # Settings Layout
        ## Main Tab
        sourceLayout = self.settingsLayout.mainTab.layout.sourceLayout
        sourceLayout.changedSource.connect(self.changeSource)
        sourceLayout.changedLoop.connect(self.mainProcessThread.mainProcess.setLoop)
        sourceLayout.changedPause.connect(self.mainProcessThread.pause)
        sourceLayout.resetCounting.connect(
            self.mainProcessThread.mainProcess.counter.reset
        )
        ## Detector Tab
        firstSection = self.settingsLayout.detectorTab.layout.firstSection
        firstSection.changedDetectorName.connect(
            self.mainProcessThread.mainProcess.setDetector
        )

        # Display Layout
        self.imageViewer = OpenCVImageViewer()
        self.mainProcessThread.changePixmap.connect(self.imageViewer.setImage)

        self.infoLayout = InfoLayout()
        self.imageViewerLayout = ImageViewerLayout(self.imageViewer)
        self.displayLayout.addLayout(self.imageViewerLayout, 0, 0)
        self.displayLayout.addLayout(self.infoLayout, 0, 1)

        mainLayout = MainLayout()
        mainLayout.addLayout(self.settingsLayout, 0, 0)
        mainLayout.addLayout(self.displayLayout, 1, 0)

        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

        self.show()

    def changeSource(self, capType, data):
        if not self.mainProcessThread.isRunning():
            self.mainProcessThread.start()

        self.mainProcessThread.setCap(capType, data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Detectors()
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainWindow = MainWindow()
    sys.exit(app.exec_())
    # mainWindow.mainProcessThread.stop()
