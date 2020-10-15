from PyQt5.QtWidgets import QVBoxLayout, QTabWidget, QWidget


class SettingsLayout(QVBoxLayout):
    def __init__(self, *args, **kwargs):
        super(SettingsLayout, self).__init__(*args, **kwargs)
        self.tabs = QTabWidget()

        self.mainTab = QWidget()
        self.detectorTab = QWidget()
        self.trackerTab = QWidget()
        self.counterTab = QWidget()

        self.tabs.addTab(self.mainTab, "Main")
        self.tabs.addTab(self.detectorTab, "Detector")
        self.tabs.addTab(self.trackerTab, "Tracker")
        self.tabs.addTab(self.counterTab, "Counter")

        self.addWidget(self.tabs)