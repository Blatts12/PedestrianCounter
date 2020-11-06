from collections.abc import Iterable
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import pyqtSignal


class GComboBox(QComboBox):
    changedValue = pyqtSignal(str)

    def __init__(self, values, placeholder="", *args, **kwargs):
        super(GComboBox, self).__init__(*args, **kwargs)
        if placeholder != "":
            self.setPlaceholderText(placeholder)

        if type(values) is str:
            self.addItem(values)
        elif isinstance(values, Iterable):
            self.addItems(values)
        self.currentTextChanged.connect(self.changedValue.emit)
