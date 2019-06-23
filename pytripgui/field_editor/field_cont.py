import logging
logger = logging.getLogger(__name__)


class FieldController(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def set_view_from_model(self):
        model = self.model
        view = self.view

        if model.is_isocenter_manually() is True:
            isocenter_values = model.get_isocenter_values()
            view.set_isocenter_values(isocenter_values)
            view.set_isocenter_state(True)
        else:
            view.set_isocenter_state(False)

        gantry_angle = model.get_gantry_angle_value()
        view.set_gantry_angle_value(gantry_angle)

        couch_angle = model.get_couch_angle_value()
        view.set_couch_angle_value(couch_angle)

        fwhm = model.get_spot_size_value()
        view.set_spot_size_value(fwhm)

        raster_step = model.get_raster_step_value()
        view.set_raster_step_value(raster_step)

        dose_extension = model.get_dose_extension_value()
        view.set_dose_extension_value(dose_extension)

        contour_extension = model.get_contour_extension_value()
        view.set_contour_extension_value(contour_extension)

        zsteps = model.get_depth_steps_value()
        view.set_depth_steps_value(zsteps)

