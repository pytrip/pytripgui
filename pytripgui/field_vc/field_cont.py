import logging
logger = logging.getLogger(__name__)


class FieldController(object):
    def __init__(self, model, view, kernels):
        self.model = model
        self.view = view
        self.kernels = kernels
        self.user_clicked_save = False

    def set_view_from_model(self):
        if self._is_isocenter_manually():
            self.view.set_isocenter_values(self.model.isocenter)
            self.view.set_isocenter_state(True)
        else:
            self.view.set_isocenter_state(False)

        self._setup_ok_and_cancel_buttons_callbacks()
        self.view.gantry_angle = self.model.gantry
        self.view.couch_angle = self.model.couch
        self.view.spot_size = self.model.fwhm
        self.view.raster_step = self.model.raster_step
        self.view.dose_extension = self.model.dose_extension
        self.view.contour_extension = self.model.contour_extension
        self.view.depth_steps = self.model.zsteps

    def _is_isocenter_manually(self):
        return len(self.model.isocenter) == 3

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
        if self.view.is_isocenter_manually():
            self.model.isocenter = self.view.get_isocenter_value()
        else:
            self.model.isocenter = []

        self.model.gantry = self.view.gantry_angle
        self.model.couch = self.view.couch_angle
        self.model.fwhm = self.view.spot_size
        self.model.raster_step = self.view.raster_step
        self.model.dose_extension = self.view.dose_extension
        self.model.contour_extension = self.view.contour_extension
        self.model.zsteps = self.view.depth_steps
