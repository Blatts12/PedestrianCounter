from PyQt5.QtWidgets import QLabel, QSlider, QGridLayout
from PyQt5.QtCore import pyqtSignal, Qt


class GSlider(QGridLayout):
    changedValue = pyqtSignal(int)

    def _sliderValueChanged(self):
        value = self.slider.value()
        self.text.setText(str(value) + self.textAfter)
        self.changedValue.emit(value)

    # desc("Slider", minium: int, maximum: int, default: int, textAfter: str)
    def __init__(self, minimum, maximum, default, text_after, *args, **kwargs):
        super(GSlider, self).__init__(*args, **kwargs)
        self.textAfter = text_after

        self.setColumnStretch(0, 92)
        self.setColumnStretch(1, 8)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(minimum, maximum)
        self.slider.setValue(default)
        self.text = QLabel(str(default) + text_after)
        self.slider.valueChanged.connect(self._sliderValueChanged)

        self.addWidget(self.slider, 0, 0)
        self.addWidget(self.text, 0, 1)
