import cv2
import os
import ipaddress
from PyQt5.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QComboBox,
    QFileDialog,
    QPushButton,
    QLineEdit,
    QMessageBox,
)
from PyQt5.QtCore import QMargins, pyqtSignal
from Project.Components.TwoPhasePushButton import TwoPhasePushButton
from Project.Components.QHLine import QHLine


class SourceLayout(QFormLayout):
    changedSource = pyqtSignal(str, str)
    changedLoop = pyqtSignal(bool)
    changedPause = pyqtSignal(bool)
    resetCounting = pyqtSignal()

    def _changeSource(self):
        source = self.sourceComboBox.currentText()
        data = ""

        if source == "Video":
            data = self.fileText.text()
            if not os.path.exists(data):
                QMessageBox.warning(
                    None, "Video", "Path isn't valid of file don't exists"
                )
                return
        elif source == "Webcam":
            data = self.webcamComboBox.currentText()
        else:
            data = self.ipText.text()
            try:
                ipaddress.ip_address(data)
            except ValueError:
                QMessageBox.warning(None, "Ip Cam", "Ip isn't valid")
                return

        self.usedSource = source
        self.changedSource.emit(source, data)

    def _changeLoop(self, loop):
        self.changedLoop.emit(loop)

    def _changePause(self, pause):
        self.changedPause.emit(pause)

    def _reset(self):
        self.resetCounting.emit()

    def __init__(self, *args, **kwargs):
        super(SourceLayout, self).__init__(*args, **kwargs)
        self.usedSource = ""
        possibleSources = ["Video", "Webcam", "Ip Cam"]

        # Source
        self.sourceComboBox = QComboBox()
        self.sourceComboBox.addItems(possibleSources)

        self.fileDialog = QFileDialog()
        self.fileButton = QPushButton("Select file")
        self.fileButton.clicked.connect(self._selectFile)
        self.fileText = QLineEdit()
        self.fileText.setPlaceholderText("Type file path")

        self.webcamComboBox = QComboBox()
        self.webcamComboBox.addItems(self._getAvalibleCameraIds())

        self.ipText = QLineEdit()
        self.ipText.setPlaceholderText("Type IP")

        self.changeButton = QPushButton("Change")
        self.changeButton.clicked.connect(self._changeSource)

        # Manipulation
        self.pauseButton = TwoPhasePushButton("Unpause", "Pause")
        self.pauseButton.phaseChanged.connect(self._changePause)
        self.resetButton = QPushButton("Reset")
        self.resetButton.clicked.connect(self._reset)
        self.loopButton = TwoPhasePushButton("No loop", "Loop")
        self.loopButton.phaseChanged.connect(self._changeLoop)

        self.addRow(QLabel("Source:"), self.sourceComboBox)
        self.addRow(self.fileButton, self.fileText)
        self.addRow(QLabel("Webcam:"), self.webcamComboBox)
        self.addRow(QLabel("Ip Cam:"), self.ipText)
        self.addRow(self.changeButton)
        self.addRow(QHLine())
        self.addRow(self.pauseButton)
        self.addRow(QHLine())
        self.addRow(QLabel("Reset counting:"), self.resetButton)
        self.addRow(QLabel("Loop video file:"), self.loopButton)

    def _selectFile(self):
        fileName = self.fileDialog.getOpenFileName(
            caption="Select file", filter="Video File (*.mp4 *.avi)"
        )
        self.fileText.setText(fileName[0])

    def _getAvalibleCameraIds(self):
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
