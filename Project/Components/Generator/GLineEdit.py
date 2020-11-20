from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtCore import pyqtSignal, Qt, QObject
from Project.Components.Generator.IGeneratorComponent import IGeneratorComponent


class GLineEdit(QObject):
    changedValue = pyqtSignal(str)
    has_buddy = True

    def __init__(self):
        super(GLineEdit, self).__init__()
        self.widget = None

    def get_widget(self):
        self.widget = QLineEdit()
        self.widget.textChanged.connect(self.changedValue.emit)

        return self.widget

    def get_buddy(self, name=""):
        return QLabel(name)