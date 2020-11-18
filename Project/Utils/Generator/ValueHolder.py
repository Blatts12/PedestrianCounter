from PyQt5.QtCore import QObject, pyqtSignal


class ValueHolder:
    def __init__(
        self,
        widget,
        default=None,
        set_value_modifier=lambda value: value,
    ):
        self.widget = widget

        self.set_value_modifier = set_value_modifier
        self.v = default

    def set_value(self, value):
        self.v = self.set_value_modifier(value)
