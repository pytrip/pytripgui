import logging
logger = logging.getLogger(__name__)


class FieldController(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def set_view_from_model(self):
        model = self.model
        view = self.view

        if self.is_isocenter_manually() is True:
            view.set_isocenter_values(model.isocenter)
            view.set_isocenter_state(True)
        else:
            view.set_isocenter_state(False)

        view.set_gantry_angle_value(model.gantry)

        view.set_couch_angle_value(model.couch)

        view.set_spot_size_value(model.fwhm)

        view.set_raster_step_value(model.raster_step)

        view.set_dose_extension_value(model.dose_extension)

        view.set_contour_extension_value(model.contour_extension)

        view.set_depth_steps_value(model.zsteps)

    def is_isocenter_manually(self):
        if len(self.model.isocenter) is 3:
            return True

        return False
