from pytrip.tripexecuter.field import Field


class FieldModel(Field):
    def __init__(self, field=Field(), display_angles_in_standard="TRiP"):
        super().__init__(field)
        self.display_angles_in_standard = display_angles_in_standard
