from PyQt5.QtWidgets import QFormLayout, QLabel
from Project.Components.Generator.GSlider import GSlider
from Project.Components.Generator.GComboBox import GComboBox
from Project.Components.Generator.GSpinBox import GSpinBox
from Project.Components.Generator.IGeneratorBase import IGeneratorBase


class SettingsFormGenerator:
    def generate(self, base):
        try:
            layout = SettingsFormLayout()

            for key, value in base.values.items():
                desc = value[1]
                widget = self._createWidget(desc)
                widget.changedValue.connect(lambda x, k=key: base.setValue(k, x))
                layout.addRowWithLabel(key, widget)

            return (base, layout)
        except Exception as e:
            raise e

    def _createWidget(self, desc):
        name = desc[0]
        if name == "Slider":
            return GSlider(desc[1], desc[2], desc[3], desc[4])
        elif name == "SpinBox":
            return GSpinBox(desc[1], desc[2], desc[3], desc[4])
        elif name == "ComboBox":
            return GComboBox(desc[1])
        return QLabel("ERROR")


class SettingsFormLayout(QFormLayout):
    def __init__(self, *args, **kwargs):
        super(SettingsFormLayout, self).__init__(*args, **kwargs)

    def addRowWithLabel(self, text, item):
        self.addRow(QLabel(text), item)
