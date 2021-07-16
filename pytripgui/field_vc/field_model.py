from pytrip.tripexecuter.field import Field

from pytripgui.field_vc.angles_standard import AnglesStandard


class FieldModel(Field):
    def __init__(self, field=Field(), display_angles_in_standard=AnglesStandard.TRIP):
        super().__init__(field)
        self.display_angles_in_standard = display_angles_in_standard
