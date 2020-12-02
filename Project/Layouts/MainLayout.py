from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtCore import QMargins


class MainLayout(QGridLayout):
    def __init__(self, *args, **kwargs):
        super(MainLayout, self).__init__(*args, **kwargs)
        self.setRowStretch(0, 290)
        self.setRowStretch(1, 660)
        self.setContentsMargins(QMargins(0, 0, 0, 0))
