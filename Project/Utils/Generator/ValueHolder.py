from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal


class ValueHolder:
    valueChanged = pyqtSignal(object)
    set_value = None

    def __init__(
        self,
        widget,
        default=None,
        set_value_modifier=lambda value: value,
        emit_change=False,
    ):
        self.widget = widget

        self.set_value_modifier = set_value_modifier
        self.v = default

        if emit_change:
            self.set_value = self.set_value_emit
        else:
            self.set_value = self.set_value_no_emit

    def set_value_no_emit(self, value):
        self.v = self.set_value_modifier(value)

    def set_value_emit(self, value):
        self.v = self.set_value_modifier(value)
        self.valueChanged.emit(self.v)
