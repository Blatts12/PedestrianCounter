from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtCore import QMargins


class DisplayLayout(QGridLayout):
    def __init__(self, *args, **kwargs):
        super(DisplayLayout, self).__init__(*args, **kwargs)
        self.setColumnStretch(0, 500)
        self.setColumnStretch(1, 300)
        self.setContentsMargins(QMargins(0, 0, 0, 0))