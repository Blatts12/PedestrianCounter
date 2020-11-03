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
        self.detector_combo_box = QComboBox()
        self.detector_combo_box.addItems(detectors)
        self.detector_combo_box.currentIndexChanged.connect(
            self.changedDetectorIndex.emit
        )
        self.detector_combo_box.currentTextChanged.connect(
            self.changedDetectorName.emit
        )

        self.addRow(QLabel("Detector:"), self.detector_combo_box)


class DetectorTabLayout(QGridLayout):
    def _changeDetector(self, index):
        self.stacked_layout.setCurrentIndex(index)

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
        self.first_section.changedDetectorIndex.connect(self._changeDetector)
        self.addLayout(self.first_section, 0, 0)
        self.addLayout(self.stacked_layout, 0, 1)
