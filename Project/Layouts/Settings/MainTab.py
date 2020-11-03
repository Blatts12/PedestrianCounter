import cv2
import os
import ipaddress
from PyQt5.QtWidgets import (
    QGridLayout,
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

    def _change_source(self):
        source = self.source_combo_box.currentText()
        data = ""

        if source == "Video":
            data = self.file_text.text()
            if not os.path.exists(data):
                QMessageBox.warning(
                    None, "Video", "Path isn't valid of file don't exists"
                )
                return
        elif source == "Webcam":
            data = self.webcam_combo_box.currentText()
        else:
            data = self.ip_text.text()
            try:
                ipaddress.ip_address(data)
            except ValueError:
                QMessageBox.warning(None, "Ip Cam", "Ip isn't valid")
                return

        self.used_source = source
        self.changedSource.emit(source, data)

    def _change_loop(self, loop):
        self.changedLoop.emit(loop)

    def _change_pause(self, pause):
        self.changedPause.emit(pause)

    def _reset(self):
        self.resetCounting.emit()

    def __init__(self, *args, **kwargs):
        super(SourceLayout, self).__init__(*args, **kwargs)
        self.used_source = ""
        possible_sources = ["Video", "Webcam", "Ip Cam"]

        # Source
        self.source_combo_box = QComboBox()
        self.source_combo_box.addItems(possible_sources)

        self.file_dialog = QFileDialog()
        self.file_button = QPushButton("Select file")
        self.file_button.clicked.connect(self._select_file)
        self.file_text = QLineEdit()
        self.file_text.setPlaceholderText("Type file path")

        self.webcam_combo_box = QComboBox()
        self.webcam_combo_box.addItems(self._get_avalible_camera_ids(20))

        self.ip_text = QLineEdit()
        self.ip_text.setPlaceholderText("Type IP")

        self.change_button = QPushButton("Change")
        self.change_button.clicked.connect(self._change_source)

        # Manipulation
        self.pause_button = TwoPhasePushButton("Unpause", "Pause")
        self.pause_button.phaseChanged.connect(self._change_pause)
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self._reset)
        self.loop_button = TwoPhasePushButton("No loop", "Loop")
        self.loop_button.phaseChanged.connect(self._change_loop)

        self.addRow(QLabel("Source:"), self.source_combo_box)
        self.addRow(self.file_button, self.file_text)
        self.addRow(QLabel("Webcam:"), self.webcam_combo_box)
        self.addRow(QLabel("Ip Cam:"), self.ip_text)
        self.addRow(self.change_button)
        self.addRow(QHLine())
        self.addRow(self.pause_button)
        self.addRow(QHLine())
        self.addRow(QLabel("Reset counting:"), self.reset_button)
        self.addRow(QLabel("Loop video file:"), self.loop_button)

    def _select_file(self):
        file_name = self.file_dialog.getOpenFileName(
            caption="Select file", filter="Video File (*.mp4 *.avi)"
        )
        if file_name[0] != "":
            self.file_text.setText(file_name[0])

    def _get_avalible_camera_ids(self, max):
        cameras = []
        for i in range(max):
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
        self.addWidget(QLabel("TODO?"))


class MainTabLayout(QGridLayout):
    def __init__(self, *args, **kwargs):
        super(MainTabLayout, self).__init__(*args, **kwargs)
        self.setColumnStretch(0, 50)
        self.setColumnStretch(1, 50)
        self.setContentsMargins(QMargins(5, 10, 5, 10))

        self.source_layout = SourceLayout()
        self.main_settings_layout = MainSettingsLayout()
        self.addLayout(self.source_layout, 0, 0)
        self.addLayout(self.main_settings_layout, 0, 1)
