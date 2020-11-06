from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtCore import pyqtSignal, Qt


class GCheckBox(QCheckBox):
    changedValue = pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super(GCheckBox, self).__init__(*args, **kwargs)
        self.stateChanged.connect(self._check_box_changed)

    def _check_box_changed(self, state):
        self.changedValue.emit(state == Qt.Checked)