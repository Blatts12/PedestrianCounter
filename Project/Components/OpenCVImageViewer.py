import vars
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap, QImage


class OpenCVImageViewer(QLabel):
    @pyqtSlot(QImage)
    def set_image(self, image):
        self.setPixmap(QPixmap.fromImage(image))

    def __init__(self, *args, **kwargs):
        super(OpenCVImageViewer, self).__init__(*args, **kwargs)
        self.resize(640, 480)
        self.set_image(vars.EMPTY_IMAGE)
