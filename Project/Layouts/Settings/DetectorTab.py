from PyQt5.QtWidgets import QComboBox, QGridLayout, QFormLayout, QLabel, QSlider
from PyQt5.QtCore import QMargins, Qt, pyqtSignal
import Project.PedestrianCounter.Detecting as Detecting


class FirstSection(QFormLayout):
    changedDetector = pyqtSignal(str)
    changedConfidence = pyqtSignal(float)
    changedNMS = pyqtSignal(float)

    def _changeDetector(self, detector):
        self.sliderConfidence.setValue(int(Detecting.DEFAULT_CONFIDENCE * 100))
        self.sliderNMS.setValue(int(Detecting.DEFAULT_NMS_THRESHOLD * 100))
        self.changedDetector.emit(detector)

    def _changeNMS(self):
        nms = self.sliderNMS.value()
        self.textNMS.setText(str(nms) + "%")
        self.changedNMS.emit(nms)

    def _changeConfidence(self):
        confidence = self.sliderConfidence.value()
        self.textConfidence.setText(str(confidence) + "%")
        self.changedConfidence.emit(confidence / 100.0)

    def __init__(self, *args, **kwargs):
        super(FirstSection, self).__init__(*args, **kwargs)
        possibleDetectors = Detecting.DETECTORS

        self.detectorComboBox = QComboBox()
        self.detectorComboBox.addItems(possibleDetectors)
        self.detectorComboBox.currentTextChanged.connect(self._changeDetector)

        self.sliderConfidence = QSlider(Qt.Horizontal)
        self.sliderConfidence.setRange(0, 100)
        self.sliderConfidence.setValue(int(Detecting.DEFAULT_CONFIDENCE * 100))
        self.sliderConfidence.valueChanged.connect(self._changeConfidence)
        self.textConfidence = QLabel(str(self.sliderConfidence.value()) + "%")
        self.gridCofidence = QGridLayout()
        self.gridCofidence.setColumnStretch(0, 93)
        self.gridCofidence.setColumnStretch(1, 7)
        self.gridCofidence.addWidget(self.sliderConfidence, 0, 0)
        self.gridCofidence.addWidget(self.textConfidence, 0, 1)

        self.sliderNMS = QSlider(Qt.Horizontal)
        self.sliderNMS.setRange(0, 100)
        self.sliderNMS.setValue(int(Detecting.DEFAULT_NMS_THRESHOLD * 100))
        self.sliderNMS.valueChanged.connect(self._changeNMS)
        self.textNMS = QLabel(str(self.sliderNMS.value()) + "%")
        self.gridNMS = QGridLayout()
        self.gridNMS.setColumnStretch(0, 93)
        self.gridNMS.setColumnStretch(1, 7)
        self.gridNMS.addWidget(self.sliderNMS, 0, 0)
        self.gridNMS.addWidget(self.textNMS, 0, 1)

        self.addRow(QLabel("Detector:"), self.detectorComboBox)
        self.addRow(QLabel("Confidence:"), self.gridCofidence)
        self.addRow(QLabel("NMS Threshold:"), self.gridNMS)


class DetectorTabLayout(QGridLayout):
    def __init__(self, *args, **kwargs):
        super(DetectorTabLayout, self).__init__(*args, **kwargs)
        self.setColumnStretch(0, 50)
        self.setColumnStretch(1, 50)
        self.setContentsMargins(QMargins(5, 10, 5, 10))

        self.firstSection = FirstSection()
        self.addLayout(self.firstSection, 0, 0)
        # self.addLayout(self.firstSection, 0, 0)