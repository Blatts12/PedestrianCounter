from PyQt5.QtWidgets import QVBoxLayout, QTabWidget, QWidget
from Project.Layouts.Settings.MainTab import MainTabLayout
from Project.Layouts.Settings.DetectorTab import DetectorTabLayout
from Project.Layouts.Settings.TrackerTab import TrackerTabLayout


class SettingsLayout(QVBoxLayout):
    def __init__(self, *args, **kwargs):
        super(SettingsLayout, self).__init__(*args, **kwargs)
        self.tabs = QTabWidget()

        self.main_tab = QWidget()
        self.detector_tab = QWidget()
        self.tracker_tab = QWidget()
        self.counter_tab = QWidget()

        self.tabs.addTab(self.main_tab, "Main")
        self.tabs.addTab(self.detector_tab, "Detector")
        self.tabs.addTab(self.tracker_tab, "Tracker")
        self.tabs.addTab(self.counter_tab, "Counter")

        self.main_tab_layout = MainTabLayout()
        self.main_tab.setLayout(self.main_tab_layout)

        self.detector_tab_layout = DetectorTabLayout()
        self.detector_tab.setLayout(self.detector_tab_layout)

        self.tracker_tab_layout = TrackerTabLayout()
        self.tracker_tab.setLayout(self.tracker_tab_layout)

        self.addWidget(self.tabs)