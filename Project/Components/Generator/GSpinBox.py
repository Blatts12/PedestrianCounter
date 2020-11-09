from PyQt5.QtWidgets import QLabel, QSpinBox
from PyQt5.QtCore import pyqtSignal, QObject
from Project.Components.Generator.IGeneratorComponent import IGeneratorComponent


class GSpinBox(QObject):
    changedValue = pyqtSignal(int)
    has_buddy = True

    def __init__(self, minimum, maximum, default, step):
        super(GSpinBox, self).__init__()
        self.minimum = minimum
        self.maximum = maximum
        self.default = default
        self.step = step
        self.widget = None

    def get_widget(self):
        self.widget = QSpinBox()
        self.widget.setRange(self.minimum, self.maximum)
        self.widget.setSingleStep(self.step)
        self.widget.setValue(self.default)

        self.widget.valueChanged.connect(self.changedValue.emit)

    def get_buddy(self, name=""):
        return QLabel(name)
