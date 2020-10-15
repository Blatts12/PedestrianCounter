from PyQt5.QtWidgets import QVBoxLayout, QLabel


class InfoLayout(QVBoxLayout):
    def __init__(self, *args, **kwargs):
        super(InfoLayout, self).__init__(*args, **kwargs)
        self.test = QLabel()
        self.test.setText("ELO")

        self.addWidget(self.test)
