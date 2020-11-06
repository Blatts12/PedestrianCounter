from PyQt5.QtWidgets import QLineEdit, QPushButton, QFileDialog
from PyQt5.QtCore import pyqtSignal


class GSelectVideoFile(QLineEdit):
    changedValue = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(GSelectVideoFile, self).__init__(*args, **kwargs)
        self.file_dialog = QFileDialog()

        self.button = QPushButton("Select file")
        self.button.clicked.connect(self._select_file)

        self.setPlaceholderText("Type file path")
        self.textChanged.connect(self.changedValue.emit)

    def _select_file(self):
        file_name = self.file_dialog.getOpenFileName(
            caption="Select file", filter="Video File (*.mp4 *.avi)"
        )
        if file_name[0] != "":
            self.setText(file_name[0])