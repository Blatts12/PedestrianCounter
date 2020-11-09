from PyQt5.QtWidgets import QLabel, QSlider, QGridLayout
from PyQt5.QtCore import pyqtSignal, Qt, QObject
from Project.Components.Generator.IGeneratorComponent import IGeneratorComponent


class GSlider(QObject):
    changedValue = pyqtSignal(int)
    has_buddy = True

    def _sliderValueChanged(self):
        value = self.slider.value()
        self.text.setText(str(value) + self.text_after)
        self.changedValue.emit(value)

    def __init__(self, minimum, maximum, default, text_after):
        super(GSlider, self).__init__()
        self.minimum = minimum
        self.maximum = maximum
        self.default = default
        self.text_after = text_after
        self.widget = None
        self.slider = None
        self.text = None

    def get_widget(self):
        self.widget = QGridLayout()
        self.widget.setColumnStretch(0, 92)
        self.widget.setColumnStretch(1, 8)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(self.minimum, self.maximum)
        self.slider.setValue(self.default)
        self.text = QLabel(str(self.default) + self.text_after)
        self.slider.valueChanged.connect(self._sliderValueChanged)

        self.widget.addWidget(self.slider, 0, 0)
        self.widget.addWidget(self.text, 0, 1)

        return self.widget

    def get_buddy(self, name=""):
        return QLabel(name)
