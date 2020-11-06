import sys
from collections.abc import Iterable
from PyQt5.QtWidgets import QFormLayout, QLabel
from Project.Components.Generator.GSlider import GSlider
from Project.Components.Generator.GComboBox import GComboBox
from Project.Components.Generator.GSpinBox import GSpinBox
from Project.Components.Generator.GSelectVideoFile import GSelectVideoFile
from Project.Components.Generator.GCheckBox import GCheckBox


class SettingsFormGenerator:
    def generate(self, base):
        try:
            layout = SettingsFormLayout()

            for value_name, value_holder in base.values.items():
                desc = value_holder.desc
                widget_pair = self._create_widget(value_name, value_holder.type, desc)
                try:
                    if isinstance(widget_pair, Iterable):
                        widget_pair[0].changedValue.connect(value_holder.set_value)
                    else:
                        widget_pair.changedValue.connect(value_holder.set_value)
                except Exception:
                    pass

                try:
                    layout.addRow(widget_pair[1], widget_pair[0])
                except Exception:
                    layout.addRow(widget_pair)

            return (base, layout)
        except Exception as e:
            raise type(e)(
                str(e)
                + "\n Class %s probably doesn't implement IGeneratorBase"
                % base.__class__.__name__
            ).with_traceback(sys.exc_info()[2])

    def _create_widget(self, name, type, desc):
        if type == "Slider":
            return (GSlider(desc[0], desc[1], desc[2], desc[3]), name)
        elif type == "SpinBox":
            return (GSpinBox(desc[0], desc[1], desc[2], desc[3]), name)
        elif type == "ComboBox":
            return (GComboBox(desc[0], desc[1]), name)
        elif type == "VideoFile":
            widget = GSelectVideoFile()
            return (widget, widget.button)
        elif type == "CheckBox":
            return GCheckBox(desc)
        elif type == "Empty":
            return QLabel("No properties to adjust")
        return QLabel("ERROR")


class SettingsFormLayout(QFormLayout):
    def __init__(self, *args, **kwargs):
        super(SettingsFormLayout, self).__init__(*args, **kwargs)

    def add_row_with_label(self, first, second):
        self.addRow(first, second)
