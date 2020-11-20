from PyQt5.QtWidgets import (
    QGridLayout,
    QFormLayout,
    QStackedLayout,
    QWidget,
    QLabel,
    QComboBox,
    QPushButton,
)
from PyQt5.QtCore import QMargins, pyqtSignal
from Project.Components.TwoPhasePushButton import TwoPhasePushButton
from Project.Components.QHLine import QHLine
from Project.PedestrianCounter.Sources import Sources


class SourceLayout(QFormLayout):
    changedSourceIndex = pyqtSignal(int)
    changedSource = pyqtSignal(str)
    changedPause = pyqtSignal(bool)
    stopClicked = pyqtSignal()
    resetCounting = pyqtSignal()

    def _changed_source(self):
        source = self.source_combo_box.currentText()
        if self.sources[source][0].ready_for_start():
            self.changedSource.emit(source)

    def __init__(self, sources, *args, **kwargs):
        super(SourceLayout, self).__init__(*args, **kwargs)
        self.sources = sources
        # Source
        self.source_combo_box = QComboBox()
        self.source_combo_box.addItems(sources)
        self.source_combo_box.currentIndexChanged.connect(self.changedSourceIndex.emit)

        self.change_button = QPushButton("Change")
        self.change_button.clicked.connect(self._changed_source)

        # Manipulation
        self.pause_button = TwoPhasePushButton("Unpaused", "Paused")
        self.pause_button.phaseChanged.connect(self.changedPause.emit)
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.resetCounting.emit)
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stopClicked.emit)

        self.addRow(QLabel("Source:"), self.source_combo_box)
        self.addRow(self.change_button)
        self.addRow(QHLine())
        self.addRow(self.pause_button)
        self.addRow(self.stop_button)
        self.addRow(QHLine())
        self.addRow(QLabel("Reset counting:"), self.reset_button)


class MainTabLayout(QGridLayout):
    def __init__(self, *args, **kwargs):
        super(MainTabLayout, self).__init__(*args, **kwargs)
        self.setColumnStretch(0, 50)
        self.setColumnStretch(1, 50)
        self.setContentsMargins(QMargins(5, 10, 5, 10))

        self.sources = Sources().DICT
        self.stacked_layout = QStackedLayout()
        for key, value in self.sources.items():
            w = QWidget()
            w.setLayout(value[1])
            self.stacked_layout.addWidget(w)

        self.source_layout = SourceLayout(self.sources)
        self.source_layout.changedSourceIndex.connect(
            self.stacked_layout.setCurrentIndex
        )
        self.addLayout(self.source_layout, 0, 0)
        self.addLayout(self.stacked_layout, 0, 1)
