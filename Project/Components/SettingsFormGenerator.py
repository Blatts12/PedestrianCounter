import sys
from PyQt5.QtWidgets import QFormLayout, QLabel


class SettingsFormGenerator:
    def generate(self, base):
        try:
            layout = QFormLayout()
            if not base.values:
                layout.addRow(QLabel("No properties to adjust"))
            else:
                for value_name, value_holder in base.values.items():
                    widget = value_holder.widget

                    if widget.has_buddy:
                        layout.addRow(
                            widget.get_buddy(value_name + ":"), widget.get_widget()
                        )
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
