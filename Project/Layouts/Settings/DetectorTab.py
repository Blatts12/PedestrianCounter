from PyQt5.QtWidgets import (
    QCheckBox,
    QComboBox,
    QGridLayout,
    QSpinBox,
    QStackedLayout,
    QFormLayout,
    QWidget,
)
from PyQt5.QtCore import QMargins, pyqtSignal, Qt
from Project.PedestrianCounter.Detecting import Detectors


class FirstSection(QFormLayout):
    changedDetectorIndex = pyqtSignal(int)
    changedDetectorName = pyqtSignal(str)
    changedSkipFrames = pyqtSignal(int)

    def __init__(self, detectors, *args, **kwargs):
        super(FirstSection, self).__init__(*args, **kwargs)
        self.detector_combo_box = QComboBox()
        self.detector_combo_box.addItems(detectors)
        self.detector_combo_box.currentIndexChanged.connect(
            self.changedDetectorIndex.emit
        )
        self.detector_combo_box.currentTextChanged.connect(
            self.changedDetectorName.emit
        )

        self.skip_frames_spinbox = QSpinBox()
        self.skip_frames_spinbox.setSingleStep(1)
        self.skip_frames_spinbox.setRange(1, 255)
        self.skip_frames_spinbox.setValue(6)
        self.skip_frames_spinbox.valueChanged.connect(self.changedSkipFrames.emit)

        self.addRow("Detector:", self.detector_combo_box)
        self.addRow("Frames to skip:", self.skip_frames_spinbox)


class DetectorTabLayout(QGridLayout):
    def __init__(self, *args, **kwargs):
        super(DetectorTabLayout, self).__init__(*args, **kwargs)
        self.detectors = Detectors().DICT
        self.setColumnStretch(0, 50)
        self.setColumnStretch(1, 50)
        self.setContentsMargins(QMargins(5, 10, 5, 10))

        self.stacked_layout = QStackedLayout()
        for key, value in self.detectors.items():
            w = QWidget()
            w.setLayout(value[1])
            self.stacked_layout.addWidget(w)

        self.first_section = FirstSection(self.detectors)
        self.first_section.changedDetectorIndex.connect(
            self.stacked_layout.setCurrentIndex
        )
        self.addLayout(self.first_section, 0, 0)
        self.addLayout(self.stacked_layout, 0, 1)
