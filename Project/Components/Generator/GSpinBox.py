from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtCore import pyqtSignal


class GSpinBox(QSpinBox):
    changedValue = pyqtSignal(int)

    # desc("SpinBox", minium: int, maximum: int, default: int, step: int)
    def __init__(self, minimum, maximum, default, step, *args, **kwargs):
        super(GSpinBox, self).__init__(*args, **kwargs)
        self.default = default

        self.setRange(minimum, maximum)
        self.setSingleStep(step)
        self.setValue(default)

        self.valueChanged.connect(self.changedValue.emit)
