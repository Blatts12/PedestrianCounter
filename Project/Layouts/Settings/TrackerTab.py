from PyQt5.QtWidgets import (
    QComboBox,
    QGridLayout,
    QSpinBox,
    QStackedLayout,
    QFormLayout,
    QLabel,
    QWidget,
)
from PyQt5.QtCore import QMargins, pyqtSignal
from Project.PedestrianCounter.Tracking import Trackers
from Project.Components.QHLine import QHLine


class FirstSection(QFormLayout):
    changedTrackerIndex = pyqtSignal(int)
    changedTrackerName = pyqtSignal(str)
    changedMaxDistance = pyqtSignal(int)
    changedMaxDisappearance = pyqtSignal(int)

    def __init__(self, trackers, *args, **kwargs):
        super(FirstSection, self).__init__(*args, **kwargs)
        self.tracker_combo_box = QComboBox()
        self.tracker_combo_box.addItems(trackers)
        self.tracker_combo_box.currentIndexChanged.connect(
            self.changedTrackerIndex.emit
        )
        self.tracker_combo_box.currentTextChanged.connect(self.changedTrackerName.emit)

        self.max_distance_spinbox = QSpinBox()
        self.max_distance_spinbox.setRange(1, 512)
        self.max_distance_spinbox.setSingleStep(1)
        self.max_distance_spinbox.setValue(36)
        self.max_distance_spinbox.valueChanged.connect(self.changedMaxDistance.emit)

        self.max_disappearance_spinbox = QSpinBox()
        self.max_disappearance_spinbox.setRange(1, 512)
        self.max_disappearance_spinbox.setSingleStep(1)
        self.max_disappearance_spinbox.setValue(36)
        self.max_disappearance_spinbox.valueChanged.connect(
            self.changedMaxDisappearance.emit
        )

        self.addRow("Tracker:", self.tracker_combo_box)
        self.addRow(QHLine())
        self.addRow(QLabel("Centroid Tracker"))
        self.addRow("Max distance: ", self.max_distance_spinbox)
        self.addRow("Max disappearance: ", self.max_disappearance_spinbox)


class TrackerTabLayout(QGridLayout):
    def __init__(self, *args, **kwargs):
        super(TrackerTabLayout, self).__init__(*args, **kwargs)
        self.trackers = Trackers().DICT
        self.setColumnStretch(0, 50)
        self.setColumnStretch(1, 50)
        self.setContentsMargins(QMargins(5, 10, 5, 10))

        self.stacked_layout = QStackedLayout()
        for key, value in self.trackers.items():
            w = QWidget()
            w.setLayout(value[1])
            self.stacked_layout.addWidget(w)

        self.first_section = FirstSection(self.trackers)
        self.first_section.changedTrackerIndex.connect(
            self.stacked_layout.setCurrentIndex
        )
        self.addLayout(self.first_section, 0, 0)
        self.addLayout(self.stacked_layout, 0, 1)
