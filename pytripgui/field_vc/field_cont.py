import logging
from pytrip.res.point import angles_to_trip, angles_from_trip

logger = logging.getLogger(__name__)


class FieldController:
    def __init__(self, model, view, kernels):
        self.model = model
        self.view = view
        self.kernels = kernels
        self.user_clicked_save = False

    def set_view_from_model(self):
        field = self.model.field

        if self._is_isocenter_manually():
            self.view.set_isocenter_values(field.isocenter)
            self.view.set_isocenter_state(True)
        else:
            self.view.set_isocenter_state(False)

        self._setup_ok_and_cancel_buttons_callbacks()

        self.view.set_angles_standard(self.model.angles_standard)

        if self.model.angles_standard == "IEC":
            gantry, couch = angles_from_trip(field.gantry, field.couch)
            self.view.gantry_angle = gantry
            self.view.couch_angle = couch
        else:
            self.view.gantry_angle = field.gantry
            self.view.couch_angle = field.couch

        self.view.spot_size = field.fwhm
        self.view.raster_step = field.raster_step
        self.view.dose_extension = field.dose_extension
        self.view.contour_extension = field.contour_extension
        self.view.depth_steps = field.zsteps

    def _is_isocenter_manually(self):
        return len(self.model.field.isocenter) == 3

    def _setup_ok_and_cancel_buttons_callbacks(self):
        self.view.set_ok_callback(self._save_and_exit)
        self.view.set_cancel_callback(self._exit)

    def _save_and_exit(self):
        self.set_model_from_view()
        self.user_clicked_save = True
        self.view.exit()

    def _exit(self):
        self.view.exit()

    def set_model_from_view(self):
        field = self.model.field
        if self.view.is_isocenter_manually():
            field.isocenter = self.view.get_isocenter_value()
        else:
            field.isocenter = []

        self.model.angles_standard = self.view.get_angles_standard()
        if self.model.angles_standard == "IEC":
            gantry, couch = angles_to_trip(self.view.gantry_angle, self.view.couch_angle)
            field.gantry = gantry
            field.couch = couch
        else:
            field.gantry = self.view.gantry_angle
            field.couch = self.view.couch_angle

        field.fwhm = self.view.spot_size
        field.raster_step = self.view.raster_step
        field.dose_extension = self.view.dose_extension
        field.contour_extension = self.view.contour_extension
        field.zsteps = self.view.depth_steps

