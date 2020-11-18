from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtCore import pyqtSignal, Qt, QObject
from Project.Components.Generator.IGeneratorComponent import IGeneratorComponent


class GCheckBox(QObject):
    changedValue = pyqtSignal(bool)
    has_buddy = False

    def __init__(self, name):
        super(GCheckBox, self).__init__()
        self.name = name
        self.widget = None

    def get_widget(self):
        self.widget = QCheckBox(self.name)
        self.widget.stateChanged.connect(
            lambda s: self.changedValue.emit(s == Qt.Checked)
        )
        return self.widget