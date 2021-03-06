from Project.Components.Generator.GSlider import GSlider
from Project.Components.Generator.GSpinBox import GSpinBox
from Project.Components.Generator.GCheckBox import GCheckBox
from PyQt5.QtWidgets import QGridLayout, QFormLayout, QCheckBox
from PyQt5.QtCore import QMargins, pyqtSignal, Qt


class FirstSection(QFormLayout):
    changedMargin = pyqtSignal(int)
    changedVectorLen = pyqtSignal(int)
    changedMinUpdate = pyqtSignal(int)
    changedInverted = pyqtSignal(bool)
    changedMotion = pyqtSignal(bool)
    changedHorizontal = pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super(FirstSection, self).__init__(*args, **kwargs)
        self.vector_len_slider = GSlider(1, 128, 16, "px")
        self.margin_slider = GSlider(0, 100, 0, "%")
        self.minimum_update_spinbox = GSpinBox(0, 255, 3, 1)
        self.count_inverted = GCheckBox("Enter direction (unchecked = up/left)")
        self.motion_vector = GCheckBox("Motion vector")

        self.vector_len_slider.changedValue.connect(self.changedVectorLen.emit)
        self.margin_slider.changedValue.connect(self.changedMargin.emit)
        self.minimum_update_spinbox.changedValue.connect(self.changedMinUpdate)
        self.count_inverted.changedValue.connect(self.changedInverted)
        self.motion_vector.changedValue.connect(self.changedMotion)

        self.horizontal_checkbox = QCheckBox()
        self.horizontal_checkbox.setText("Horizontal counting")
        self.horizontal_checkbox.stateChanged.connect(
            lambda s: self.changedHorizontal.emit(s == Qt.Checked)
        )

        self.addRow("Vector Length:", self.vector_len_slider.get_widget())
        self.addRow("Margin:", self.margin_slider.get_widget())
        self.addRow("Minium updates:", self.minimum_update_spinbox.get_widget())
        self.addRow(self.count_inverted.get_widget())
        self.addRow(self.motion_vector.get_widget())
        self.addRow(self.horizontal_checkbox)


class CounterTabLayout(QGridLayout):
    def __init__(self, *args, **kwargs):
        super(CounterTabLayout, self).__init__(*args, **kwargs)
        self.setColumnStretch(0, 50)
        self.setColumnStretch(1, 50)
        self.setContentsMargins(QMargins(5, 10, 5, 10))

        self.first_section = FirstSection()

        self.addLayout(self.first_section, 0, 0)
