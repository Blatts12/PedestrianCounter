from PyQt5.QtWidgets import QLabel, QPixmap
from PyQt5.QtCore import pyqtSlot


class OpenCVImageViewer(QLabel):
    @pyqtSlot(QImage)
    def setImage(self, image):
        self.setPixmap(QPixmap.fromImage(image))

    def __init__(self, *args, **kwargs):
        super(OpenCVImageViewer, self).__init__(*args, **kwargs)
        self.resize(640, 480)
