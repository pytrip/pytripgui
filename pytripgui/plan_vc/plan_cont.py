import logging
logger = logging.getLogger(__name__)


class PlanController(object):
    def __init__(self, model, view, kernels, patient_vdx):
        self.model = model
        self.view = view
        self.kernels = kernels
        self.user_clicked_save = False
        self.vdx = patient_vdx

    def set_view_from_model(self):
        model = self.model
        view = self.view

        self._setup_ok_and_cancel_buttons_callbacks()
        view.set_basename_value(model.basename)
        view.set_comment_value(model.comment)
        view.set_uuid_value(str(model.__uuid__))
        self._setup_target_roi()
        self._setup_oar()
        self._setup_target_tissue()
        self._setup_residual_tissue()
        self._setup_kernels()

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

        model.basename = view.get_basename_value()
        model.comment = view.get_comment_value()
        # model.__uuid__ = view.get_uuid_value()
        model.voi_target = view.get_selected_target_roi()

    def _setup_target_roi(self):
        self._fill_view_with_rois()
        self._set_correct_target_roi_view()

    def _fill_view_with_rois(self):
        view = self.view

        for voi in self.vdx.vois:
            view.add_target_roi_with_name(voi, voi.name)

    def _set_correct_target_roi_view(self):
        model = self.model
        view = self.view

        if model.voi_target is not None:
            view.set_target_roi_to_this(model.voi_target)

    def _setup_oar(self):
        self._fill_view_with_oars()
        self._mark_specified_oars_as_checked()

    def _fill_view_with_oars(self):
        view = self.view

        for voi in self.vdx.vois:
            view.add_oar_with_name(voi, voi.name)

    def _mark_specified_oars_as_checked(self):
        pass        # TODO

    def _setup_target_tissue(self):
        pass        # TODO

    def _setup_residual_tissue(self):
        pass        # TODO

    def _setup_kernels(self):
        view = self.view
        model = self.model
        kernels = self.kernels

        for kernel in kernels:
            view.add_kernel_with_name(kernel, kernel.name)

        view.select_kernel_view_to_this(model.kernel)
