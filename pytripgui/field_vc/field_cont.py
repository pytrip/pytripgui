import logging
logger = logging.getLogger(__name__)


class FieldController(object):
    def __init__(self, model, view, kernels):
        self.model = model
        self.view = view
        self.kernels = kernels
        self.user_clicked_save = False

    def set_view_from_model(self):
        model = self.model
        view = self.view

        if self._is_isocenter_manually():
            view.set_isocenter_values(model.isocenter)
            view.set_isocenter_state(True)
        else:
            view.set_isocenter_state(False)

        self._setup_ok_and_cancel_buttons_callbacks()
        view.set_gantry_angle_value(model.gantry)
        view.set_couch_angle_value(model.couch)
        view.set_spot_size_value(model.fwhm)
        view.set_raster_step_value(model.raster_step)
        view.set_dose_extension_value(model.dose_extension)
        view.set_contour_extension_value(model.contour_extension)
        view.set_depth_steps_value(model.zsteps)
        self._setup_kernels()

    def _is_isocenter_manually(self):
        return len(self.model.isocenter) == 3

    def _setup_kernels(self):
        view = self.view
        model = self.model
        kernels = self.kernels

        for kernel in kernels:
            view.add_kernel_with_name(kernel, kernel.name)

        view.set_kernel_view_to_this(model.kernel)

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
        model = self.model
        view = self.view

        if view.is_isocenter_manually():
            model.isocenter = view.get_isocenter_value()
        else:
            model.isocenter = []

        model.gantry = view.get_gantry_angle_value()
        model.couch = view.get_couch_angle_value()
        model.fwhm = view.get_spot_size_value()
        model.raster_step = view.get_raster_step_value()
        model.dose_extension = view.get_dose_extension_value()
        model.contour_extension = view.get_contour_extension_value()
        model.zsteps = view.get_depth_steps_value()
        model.kernel = view.get_selected_kernel()
