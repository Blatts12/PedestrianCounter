import sys
from PyQt5.QtWidgets import QFormLayout, QLabel
from Project.Components.Generator.GSlider import GSlider
from Project.Components.Generator.GComboBox import GComboBox
from Project.Components.Generator.GSpinBox import GSpinBox


class SettingsFormGenerator:
    def generate(self, base):
        try:
            layout = SettingsFormLayout()

            for key, value in base.values.items():
                desc = value[1]
                widget = self._create_widget(desc)
                try:
                    widget.changedValue.connect(lambda x, k=key: base.set_value(k, x))
                except Exception:
                    pass
                layout.add_row_with_label(key, widget)

            return (base, layout)
        except Exception as e:
            raise type(e)(
                str(e)
                + "\n Class %s probably doesn't implement IGeneratorBase"
                % base.__class__.__name__
            ).with_traceback(sys.exc_info()[2])

    def _create_widget(self, desc):
        name = desc[0]
        if name == "Slider":
            return GSlider(desc[1], desc[2], desc[3], desc[4])
        elif name == "SpinBox":
            return GSpinBox(desc[1], desc[2], desc[3], desc[4])
        elif name == "ComboBox":
            return GComboBox(desc[1])
        elif name == "None":
            return QLabel()
        return QLabel("ERROR")


class SettingsFormLayout(QFormLayout):
    def __init__(self, *args, **kwargs):
        super(SettingsFormLayout, self).__init__(*args, **kwargs)

    def add_row_with_label(self, text, item):
        self.addRow(QLabel(text), item)
