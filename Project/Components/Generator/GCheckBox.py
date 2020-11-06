from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtCore import pyqtSignal, Qt


class GCheckBox(QCheckBox):
    changedValue = pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super(GCheckBox, self).__init__(*args, **kwargs)
        self.stateChanged.connect(lambda s: self.changedValue.emit(s == Qt.Checked))