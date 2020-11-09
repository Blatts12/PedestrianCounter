from PyQt5.QtWidgets import QLineEdit, QPushButton, QFileDialog
from PyQt5.QtCore import QObject, pyqtSignal
from Project.Components.Generator.IGeneratorComponent import IGeneratorComponent


class GSelectVideoFile(QObject):
    changedValue = pyqtSignal(str)
    has_buddy = True

    def __init__(self):
        super(GSelectVideoFile, self).__init__()
        self.file_dialog = None
        self.button = None
        self.widget = None

    def get_widget(self):
        self.widget = QLineEdit()
        self.file_dialog = QFileDialog()

        self.widget.setPlaceholderText("Type file path")
        self.widget.textChanged.connect(self.changedValue.emit)

        return self.widget

    def get_buddy(self, name=""):
        self.button = QPushButton("Select file")
        self.button.clicked.connect(self._select_file)
        return self.button

    def _select_file(self):
        file_name = self.file_dialog.getOpenFileName(
            caption="Select file", filter="Video File (*.mp4 *.avi)"
        )
        if file_name[0] != "":
            self.widget.setText(file_name[0])