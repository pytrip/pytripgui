import logging
logger = logging.getLogger(__name__)


class FieldController(object):
    def __init__(self, model, view, kernels):
        self.model = model
        self.view = view
        self.kernels = kernels
        self.save_data = False

    def set_view_from_model(self):
        model = self.model
        view = self.view

        if self._is_isocenter_manually():
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
        self._fill_view_with_kernels()
        self._set_view_to_chosen_kernel()
        self._setup_ok_and_cancel_buttons_callbacks()

    def _is_isocenter_manually(self):
        return len(self.model.isocenter) == 3

    def _fill_view_with_kernels(self):
        view = self.view
        kernels = self.kernels

        for kernel in kernels:
            view.add_kernel_with_name(kernel, kernel.name)

    def _set_view_to_chosen_kernel(self):
        model = self.model
        view = self.view

        view.set_kernel_view_to_this(model.kernel)

    def _setup_ok_and_cancel_buttons_callbacks(self):
        self.view.set_ok_callback(self._save_this_field)
        self.view.set_cancel_callback(self._dont_save_this_field)

    def _save_this_field(self):
        self.set_model_from_view()
        self.save_data = True
        self.view.exit()

    def _dont_save_this_field(self):
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
