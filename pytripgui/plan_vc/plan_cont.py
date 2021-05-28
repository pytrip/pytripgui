import logging

from pytripgui.messages import InfoMessages

logger = logging.getLogger(__name__)


class PlanController:
    def __init__(self, model, view, kernels, patient_vois):
        self.model = model
        self.view = view
        self.kernels = kernels
        self.user_clicked_save = False
        self.vois = patient_vois

    def set_view_from_model(self):
        self._setup_ok_and_cancel_buttons_callbacks()

        self.view.basename = self.model.basename
        self.view.comment = self.model.comment
        self.view.uuid = str(self.model.__uuid__)

        self._setup_target_roi()
        self._setup_oar()

        self._setup_kernels()
        self.view.target_dose = self.model.target_dose
        self.view.relative_target_dose = self.model.target_dose_percent

        self.view.iterations = self.model.iterations
        self.view.eps = self.model.eps
        self.view.geps = self.model.geps
        self._setup_optimization_metod()
        self._setup_principle()
        self._setup_dose_algorithm()
        self._setup_biological_algorithm()
        self._setup_opti_algorithm()

        self.view.physical_dose_dist = self.model.want_phys_dose
        self.view.biological_dose_dist = self.model.want_bio_dose
        self.view.dose_averaged_let = self.model.want_dlet
        self.view.raster_scan_file = self.model.want_rst

        self.view.set_unimplemented_fields_disabled()

    def _setup_ok_and_cancel_buttons_callbacks(self):
        self.view.set_ok_callback(self._save_and_exit)
        self.view.set_cancel_callback(self._exit)

    def _save_and_exit(self):
        if not self.view.get_selected_target_roi():
            self.view.show_info(*InfoMessages['noTargetRoiSelected'])
            return
        self.set_model_from_view()
        self.user_clicked_save = True
        self.view.exit()

    def _exit(self):
        self.view.exit()

    def set_model_from_view(self):
        self.model.basename = self.view.basename
        self.model.comment = self.view.comment

        self.model.voi_target = self.view.get_selected_target_roi()
        self.model.vois_oar = self.view.get_all_checked_oar_as_list()

        self.model.default_kernel = self.view.get_selected_krenel()
        self.model.target_dose = self.view.target_dose
        self.model.target_dose_percent = self.view.relative_target_dose

        self.model.iterations = self.view.iterations
        self.model.eps = self.view.eps
        self.model.geps = self.view.geps
        self.model.opt_method = self.view.get_selected_opti_method()
        self.model.opt_principle = self.view.get_selected_principle()
        self.model.dose_alg = self.view.get_selected_dose_algorithm()
        self.model.bio_alg = self.view.get_selected_bio_algorithm()
        self.model.opt_alg = self.view.get_selected_opti_algorithm()

        self.model.want_phys_dose = self.view.physical_dose_dist
        self.model.want_bio_dose = self.view.biological_dose_dist
        self.model.want_dlet = self.view.dose_averaged_let
        self.model.want_rst = self.view.raster_scan_file

    def _setup_target_roi(self):
        if not self.vois:
            return
        for voi in self.vois:
            checked = self.model.voi_target == voi
            self.view.add_target_roi_with_name(voi, voi.name, checked)

    def _setup_oar(self):
        self._fill_view_with_oars()
        self._mark_specified_oars_as_checked()

    def _fill_view_with_oars(self):
        if not self.vois:
            return
        for voi in self.vois:
            self.view.add_oar_with_name(voi, voi.name)

    def _mark_specified_oars_as_checked(self):
        for oar in self.model.vois_oar:
            self.view.set_oar_as_checked(oar)

    def _setup_kernels(self):
        if not self.kernels:
            logger.error("You should first setup kernels with: Settings -> beam kernels")
            return

        for kernel in self.kernels:
            self.view.add_kernel_with_name(kernel, kernel.name)

        self.view.select_kernel_view_to_this(self.model.default_kernel)

    def _setup_optimization_metod(self):
        opt_methods = self.model.opt_methods

        for short_name, (_, full_name, _) in opt_methods.items():
            self.view.add_opti_method_with_name(short_name, full_name)

        self.view.select_opti_method_view_to_this(self.model.opt_method)

    def _setup_principle(self):
        principles = self.model.opt_principles

        for short_name, (_, full_name, _) in principles.items():
            self.view.add_principle_with_name(short_name, full_name)

        self.view.select_principle_view_to_this(self.model.opt_principle)

    def _setup_dose_algorithm(self):
        dose_algs = self.model.dose_algs

        for short_name, (_, full_name, _) in dose_algs.items():
            self.view.add_dose_algorithm_with_name(short_name, full_name)

        self.view.select_dose_algorithm_view_to_this(self.model.dose_alg)

    def _setup_biological_algorithm(self):
        bio_algs = self.model.bio_algs

        for short_name, (_, full_name, _) in bio_algs.items():
            self.view.add_bio_algorithm_with_name(short_name, full_name)

        self.view.select_bio_algorithm_view_to_this(self.model.bio_alg)

    def _setup_opti_algorithm(self):
        opti_algs = self.model.opt_algs

        for short_name, (_, full_name, _) in opti_algs.items():
            self.view.add_opti_algorithm_with_name(short_name, full_name)

        self.view.select_opti_algorithm_view_to_this(self.model.opt_alg)
