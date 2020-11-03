from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSignal


class TwoPhasePushButton(QPushButton):
    phaseChanged = pyqtSignal(bool)

    def c(self):
        if self.changed:
            self.changed = False
            self.setText(self.first)
        else:
            self.changed = True
            self.setText(self.second)
        self.phaseChanged.emit(self.changed)

    def __init__(self, first, second):
        super(TwoPhasePushButton, self).__init__()
        self.first = first
        self.second = second
        self.changed = False
        self.setText(self.first)
        self.clicked.connect(self.c)
