from PyQt5.QtWidgets import (
    QComboBox,
    QGridLayout,
    QStackedLayout,
    QFormLayout,
    QLabel,
    QWidget,
)
from PyQt5.QtCore import QMargins, pyqtSignal
from Project.PedestrianCounter.Detecting import Detectors


class FirstSection(QFormLayout):
    changedDetectorIndex = pyqtSignal(int)
    changedDetectorName = pyqtSignal(str)

    def __init__(self, detectors, *args, **kwargs):
        super(FirstSection, self).__init__(*args, **kwargs)
        self.detectorComboBox = QComboBox()
        self.detectorComboBox.addItems(detectors)
        self.detectorComboBox.currentIndexChanged.connect(
            self.changedDetectorIndex.emit
        )
        self.detectorComboBox.currentTextChanged.connect(self.changedDetectorName.emit)

        self.addRow(QLabel("Detector:"), self.detectorComboBox)


class DetectorTabLayout(QGridLayout):
    def _changeDetector(self, index):
        self.stackedLayout.setCurrentIndex(index)

    def __init__(self, *args, **kwargs):
        super(DetectorTabLayout, self).__init__(*args, **kwargs)
        self.detectors = Detectors().DICT
        self.setColumnStretch(0, 50)
        self.setColumnStretch(1, 50)
        self.setContentsMargins(QMargins(5, 10, 5, 10))

        self.stackedLayout = QStackedLayout()
        for key, value in self.detectors.items():
            w = QWidget()
            w.setLayout(value[1])
            self.stackedLayout.addWidget(w)

        self.firstSection = FirstSection(self.detectors)
        self.firstSection.changedDetectorIndex.connect(self._changeDetector)
        self.addLayout(self.firstSection, 0, 0)
        self.addLayout(self.stackedLayout, 0, 1)
