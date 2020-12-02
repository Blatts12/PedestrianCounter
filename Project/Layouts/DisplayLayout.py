from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtCore import Qt


class DisplayLayout(QHBoxLayout):
    def __init__(self, *args, **kwargs):
        super(DisplayLayout, self).__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignCenter)