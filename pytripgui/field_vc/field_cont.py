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
        view.gantry_angle = model.gantry
        view.couch_angle = model.couch
        view.spot_size = model.fwhm
        view.raster_step = model.raster_step
        view.dose_extension = model.dose_extension
        view.contour_extension = model.contour_extension
        view.depth_steps = model.zsteps
        self._setup_kernels()

    def _is_isocenter_manually(self):
        return len(self.model.isocenter) == 3

    def _setup_kernels(self):
        view = self.view
        model = self.model
        kernels = self.kernels

        for kernel in kernels:
            view.add_kernel_with_name(kernel, kernel.name)

        view.select_kernel_view_to_this(model.kernel)

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

        model.gantry = view.gantry_angle
        model.couch = view.couch_angle
        model.fwhm = view.spot_size
        model.raster_step = view.raster_step
        model.dose_extension = view.dose_extension
        model.contour_extension = view.contour_extension
        model.zsteps = view.depth_steps
        model.kernel = view.selected_kernel
