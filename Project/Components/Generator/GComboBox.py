from collections.abc import Iterable
from PyQt5.QtWidgets import QComboBox, QLabel
from PyQt5.QtCore import pyqtSignal, QObject
from Project.Components.Generator.IGeneratorComponent import IGeneratorComponent


class GComboBox(QObject):
    changedValue = pyqtSignal(str)
    has_buddy = True

    def __init__(self, values, placeholder=""):
        super(GComboBox, self).__init__()
        self.values = values
        self.placeholder = placeholder
        self.widget = None

    def get_widget(self):
        self.widget = QComboBox()
        self.widget.setPlaceholderText(self.placeholder)

        if type(self.values) is str:
            self.widget.addItem(self.values)
        elif isinstance(self.values, Iterable):
            self.widget.addItems(self.values)
        self.widget.currentIndexChanged.connect(self.changedValue.emit)

        return self.widget

    def get_buddy(self, name=""):
        return QLabel(name)
