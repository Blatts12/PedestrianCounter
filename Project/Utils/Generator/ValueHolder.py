class ValueHolder:
    def __init__(
        self,
        type="Empty",
        desc=(),
        default=None,
        set_value_modifier=lambda value: value,
    ):
        self.desc = desc
        self.type = type

        self.set_value_modifier = set_value_modifier
        self.v = default

    def set_value(self, value):
        self.v = self.set_value_modifier(value)
