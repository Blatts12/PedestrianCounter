from PyQt5.QtWidgets import (
    QComboBox,
    QGridLayout,
    QStackedLayout,
    QFormLayout,
    QLabel,
    QWidget,
)
from PyQt5.QtCore import QMargins, pyqtSignal
from Project.PedestrianCounter.Tracking import Trackers


class FirstSection(QFormLayout):
    changedTrackerIndex = pyqtSignal(int)
    changedTrackerName = pyqtSignal(str)

    def __init__(self, trackers, *args, **kwargs):
        super(FirstSection, self).__init__(*args, **kwargs)
        self.tracker_combo_box = QComboBox()
        self.tracker_combo_box.addItems(trackers)
        self.tracker_combo_box.currentIndexChanged.connect(
            self.changedTrackerIndex.emit
        )
        self.tracker_combo_box.currentTextChanged.connect(self.changedTrackerName.emit)

        self.addRow(QLabel("Tracker:"), self.tracker_combo_box)


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
