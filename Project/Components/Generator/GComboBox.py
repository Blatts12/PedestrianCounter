from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import pyqtSignal


class GComboBox(QComboBox):
    changedValue = pyqtSignal(str)

    # desc("ComboBox", values: list)
    def __init__(self, values, *args, **kwargs):
        super(GComboBox, self).__init__(*args, **kwargs)
        self.addItems(values)
        self.currentTextChanged.connect(self.changedValue.emit)
