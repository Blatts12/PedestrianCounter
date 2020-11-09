import sys
from PyQt5.QtWidgets import QFormLayout, QLabel


class SettingsFormGenerator:
    def generate(self, base):
        try:
            layout = SettingsFormLayout()
            if not base.values:
                layout.addRow(QLabel("No properties to adjust"))
            else:
                for value_name, value_holder in base.values.items():
                    widget = value_holder.widget

                    if widget.has_buddy:
                        layout.addRow(widget.get_buddy(value_name), widget.get_widget())
                    else:
                        layout.addRow(widget.get_widget())

                    try:
                        widget.changedValue.connect(value_holder.set_value)
                    except Exception:
                        pass

            return (base, layout)
        except Exception as e:
            raise type(e)(
                str(e)
                + "\n Class %s probably doesn't implement IGeneratorBase"
                % base.__class__.__name__
            ).with_traceback(sys.exc_info()[2])

    # def _create_widget(self, name, type, desc):
    #     if type == "Slider":
    #         return (GSlider(desc[0], desc[1], desc[2], desc[3]), name)
    #     elif type == "SpinBox":
    #         return (GSpinBox(desc[0], desc[1], desc[2], desc[3]), name)
    #     elif type == "ComboBox":
    #         return (GComboBox(desc[0], desc[1]), name)
    #     elif type == "VideoFile":
    #         widget = GSelectVideoFile()
    #         return (widget, widget.button)
    #     elif type == "CheckBox":
    #         return GCheckBox(desc)
    #     elif type == "Empty":
    #         return QLabel("No properties to adjust")
    #     return QLabel("ERROR")


class SettingsFormLayout(QFormLayout):
    def __init__(self, *args, **kwargs):
        super(SettingsFormLayout, self).__init__(*args, **kwargs)

    def add_row_with_label(self, first, second):
        self.addRow(first, second)
