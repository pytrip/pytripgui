from pytrip.tripexecuter.field import Field


class FieldModel:
    def __init__(self, field=Field(), angles_standard="TRiP"):
        self.field = field
        self.angles_standard = angles_standard
