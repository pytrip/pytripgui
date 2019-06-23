from pytrip.tripexecuter import Field

import logging
logger = logging.getLogger(__name__)


class FieldModel(object):
    def __init__(self, field=None):
        if field is None:
            self.field = Field()
        else:
            self.field = field

        self.field_test()

    def field_test(self):
        field = self.field

        lenth_of_isocenter = len(field.isocenter)
        if lenth_of_isocenter is not 0 and lenth_of_isocenter is not 3:
            raise Exception("Field.isocenter length is({}) instead of 0 or 3".format(lenth_of_isocenter))

    def set_isocenter_manually(self, bool):
        if bool is True:
            self.field.isocenter = [0.0, 0.0, 0.0]
        else:
            self.field.isocenter = []

    def is_isocenter_manually(self):
        if len(self.field.isocenter) is 3:
            return True

        return False

    def get_isocenter_values(self):
        if self.is_isocenter_manually() is False:
            raise Exception("isocenter will be set automatically")
        return self.field.isocenter

    def set_isocenter_values(self, isocenter):
        if self.is_isocenter_manually() is False:
            raise Exception("isocenter will be set automatically")
        self.field.isocenter = isocenter

    def get_gantry_angle_value(self):
        return self.field.gantry

    def set_gantry_angle_value(self, gantry_angle):
        self.field.gantry = gantry_angle

    def get_couch_angle_value(self):
        return self.field.couch

    def set_couch_angle_value(self, couch_angle):
        self.field.couch = couch_angle

    def get_spot_size_value(self):
        return self.field.fwhm

    def set_spot_size_value(self, spot_size):
        self.field.fwhm = spot_size

    def get_raster_step_value(self):
        return self.field.raster_step

    def set_raster_step_value(self, raster_step):
        self.field.raster_step = raster_step

    def get_dose_extension_value(self):
        return self.field.dose_extension

    def set_dose_extension_value(self, dose_extension):
        self.field.dose_extension = dose_extension

    def get_contour_extension_value(self):
        return self.field.contour_extension

    def set_contour_extension_value(self, contour_extension):
        self.field.contour_extension = contour_extension

    def get_depth_steps_value(self):
        return self.field.zsteps

    def set_depth_steps_value(self, zsteps):
        self.field.zsteps = zsteps
