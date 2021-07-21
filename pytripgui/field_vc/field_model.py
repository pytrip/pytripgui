from pytrip.tripexecuter.field import Field

from pytripgui.field_vc.angles_standard import AnglesStandard


class FieldModel(Field):
    def __init__(self, field=Field(), angles_standard=AnglesStandard.TRIP):
        super().__init__(field)
        self.angles_standard = angles_standard

    @property
    def gantry_angle_trip98(self):
        return self.gantry

    @property
    def couch_angle_trip98(self):
        return self.couch

    @gantry_angle_trip98.setter
    def gantry_angle_trip98(self, angle):
        self.gantry = angle

    @couch_angle_trip98.setter
    def couch_angle_trip98(self, angle):
        self.couch = angle
