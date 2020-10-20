import cv2
from PyQt5.QtWidgets import (
    QGridLayout,
    QLabel,
    QComboBox,
    QFormLayout,
    QFileDialog,
    QPushButton,
    QLineEdit,
)
from PyQt5.QtCore import QMargins, pyqtSignal

# from enum import Enum

# class Source(Enum):
#     VIDEO = "Video"


class SourceLayout(QFormLayout):
    selectedFile = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(SourceLayout, self).__init__(*args, **kwargs)
        possibleSources = ["Video", "Webcam", "Ip Cam"]

        self.sourceComboBox = QComboBox()
        self.sourceComboBox.setPlaceholderText("Select source")
        self.sourceComboBox.addItems(possibleSources)
        # self.sourceComboBox.currentTextChanged.connect(self.changeSource)

        self.fileDialog = QFileDialog()
        self.fileButton = QPushButton("Select file")
        self.fileButton.clicked.connect(self.selectFile)
        self.fileText = QLineEdit()
        self.fileText.setPlaceholderText("Type file path")

        self.webcamComboBox = QComboBox()
        self.webcamComboBox.setPlaceholderText("Select webcam id")
        self.webcamComboBox.addItems(self.getAvalibleCameraIds())
        # self.webcamComboBox.currentIndexChanged.connect(self.changeWebcam)

        self.ipText = QLineEdit()
        self.ipText.setPlaceholderText("Type IP")

        self.addRow(QLabel("Source:"), self.sourceComboBox)
        self.addRow(self.fileButton, self.fileText)
        self.addRow(QLabel("Webcam:"), self.webcamComboBox)
        self.addRow(QLabel("Ip Cam:"), self.ipText)

    def selectFile(self):
        fileName = self.fileDialog.getOpenFileName(
            caption="Select file", filter="Video File (*.mp4 *.avi)"
        )
        self.fileText.setText(fileName[0])
        self.selectedFile.emit(fileName[0])

    def getAvalibleCameraIds(self):
        cameras = []
        for i in range(20):
            cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            if cap is not None and cap.isOpened():
                cameras.append(str(i))
            cap.release()

        return cameras


class MainSettingsLayout(QFormLayout):
    def __init__(self, *args, **kwargs):
        super(MainSettingsLayout, self).__init__(*args, **kwargs)
        self.addWidget(QLabel("AEEE"))


class MainTabLayout(QGridLayout):
    def __init__(self, *args, **kwargs):
        super(MainTabLayout, self).__init__(*args, **kwargs)
        self.setColumnStretch(0, 50)
        self.setColumnStretch(1, 50)
        self.setContentsMargins(QMargins(5, 10, 5, 10))

        self.sourceLayout = SourceLayout()
        self.mainSettingsLayout = MainSettingsLayout()
        self.addLayout(self.sourceLayout, 0, 0)
        self.addLayout(self.mainSettingsLayout, 0, 1)
