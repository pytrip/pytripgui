import logging
logger = logging.getLogger(__name__)


class PlanController(object):
    def __init__(self, model, view, kernels, patient_vois):
        self.model = model
        self.view = view
        self.kernels = kernels
        self.user_clicked_save = False
        self.vois = patient_vois

    def set_view_from_model(self):
        model = self.model
        view = self.view

        self._setup_ok_and_cancel_buttons_callbacks()

        view.basename = model.basename
        view.comment = model.comment
        view.uuid = str(model.__uuid__)

        self._setup_target_roi()
        self._setup_oar()

        self._setup_kernels()
        view.target_dose = model.target_dose
        view.relative_target_dose = model.target_dose_percent

        view.iterations = model.iterations
        view.eps = model.eps
        view.geps = model.geps
        self._setup_optimization_metod()
        self._setup_principle()
        self._setup_dose_algorithm()
        self._setup_biological_algorithm()
        self._setup_opti_algorithm()

        view.physical_dose_dist = model.want_phys_dose
        view.biological_dose_dist = model.want_bio_dose
        view.dose_averaged_let = model.want_dlet
        view.raster_scan_file = model.want_rst

        view.set_unimplemented_fields_disabled()

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

        model.basename = view.basename
        model.comment = view.comment

        model.voi_target = view.get_selected_target_roi()
        self.model.vois_oar = view.get_all_checked_oar_as_list()

        model.kernel = view.get_selected_krenel()
        model.target_dose = view.target_dose
        model.target_dose_percent = view.relative_target_dose

        model.iterations = view.iterations
        model.eps = view.eps
        model.geps = view.geps
        model.opt_method = view.get_selected_opti_method()
        model.opt_principle = view.get_selected_principle()
        model.dose_alg = view.get_selected_dose_algorithm()
        model.bio_alg = view.get_selected_bio_algorithm()
        model.opt_alg = view.get_selected_opti_algorithm()

        model.want_phys_dose = view.physical_dose_dist
        model.want_bio_dose = view.biological_dose_dist
        model.want_dlet = view.dose_averaged_let
        model.want_rst = view.raster_scan_file

    def _setup_target_roi(self):
        self._fill_view_with_rois()
        self._set_correct_target_roi_view()

    def _fill_view_with_rois(self):
        view = self.view

        for voi in self.vois:
            view.add_target_roi_with_name(voi, voi.name)

    def _set_correct_target_roi_view(self):
        model = self.model
        view = self.view

        if model.voi_target is not None:
            view.select_target_roi_to_this(model.voi_target)

    def _setup_oar(self):
        self._fill_view_with_oars()
        self._mark_specified_oars_as_checked()

    def _fill_view_with_oars(self):
        view = self.view

        for voi in self.vois:
            view.add_oar_with_name(voi, voi.name)

    def _mark_specified_oars_as_checked(self):
        for oar in self.model.vois_oar:
            self.view.set_oar_as_checked(oar)

    def _setup_kernels(self):
        view = self.view
        model = self.model
        kernels = self.kernels

        kernel_exception = "You should first setup kernels with: Settings -> beam kernels"
        try:
            if len(kernels) == 0:
                raise Exception(kernel_exception)
        except TypeError:
            raise Exception(kernel_exception)

        for kernel in kernels:
            view.add_kernel_with_name(kernel, kernel.name)

        view.select_kernel_view_to_this(model.kernel)

    def _setup_optimization_metod(self):
        view = self.view
        opt_methods = self.model.opt_methods

        for short_name, (_, full_name, _) in opt_methods.items():
            view.add_opti_method_with_name(short_name, full_name)

        view.select_opti_method_view_to_this(self.model.opt_method)

    def _setup_principle(self):
        view = self.view
        principles = self.model.opt_principles

        for short_name, (_, full_name, _) in principles.items():
            view.add_principle_with_name(short_name, full_name)

        view.select_principle_view_to_this(self.model.opt_principle)

    def _setup_dose_algorithm(self):
        view = self.view
        dose_algs = self.model.dose_algs

        for short_name, (_, full_name, _) in dose_algs.items():
            view.add_dose_algorithm_with_name(short_name, full_name)

        view.select_dose_algorithm_view_to_this(self.model.dose_alg)

    def _setup_biological_algorithm(self):
        view = self.view
        bio_algs = self.model.bio_algs

        for short_name, (_, full_name, _) in bio_algs.items():
            view.add_bio_algorithm_with_name(short_name, full_name)

        view.select_bio_algorithm_view_to_this(self.model.bio_alg)

    def _setup_opti_algorithm(self):
        view = self.view
        opti_algs = self.model.opt_algs

        for short_name, (_, full_name, _) in opti_algs.items():
            view.add_opti_algorithm_with_name(short_name, full_name)

        view.select_opti_algorithm_view_to_this(self.model.opt_alg)
