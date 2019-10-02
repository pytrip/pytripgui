from pytripgui.controller.settings_cont import SettingsController
import os

from pytripgui.treewidget_vc.treewidget_cont import TreeWidgetController
from pytripgui.Patient.patient_gui_model import PatientGui

from pytripgui.viewcanvas_vc.viewcanvas_cont import ViewCanvasCont
from pytripgui.model.plot_model import PlotModel

from pytripgui.messages import InfoMessages
import logging
logger = logging.getLogger(__name__)


class MainWindowController(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self._initialize()

        # debug
        patient = self.on_add_new_patient()
        self.model.patient_tree_cont.synchronize()

        filename = "/home/deerjelen/guit/TST000000"
        patient.open_ctx(filename + ".ctx")  # Todo catch exceptions
        patient.open_vdx(filename + ".vdx")  # Todo catch exceptions

        self.model.patient_tree_cont.synchronize()
        self.model.one_plot_cont.set_patient(self.model.current_patient)

    def open_files(self, args):
        pass
        # raise Exception("Unimplemented")  # TODO

    def _initialize(self):
        self.settings = SettingsController(self.model)

        # main window callbacks
        self.view.open_voxelplan_callback = self.on_open_voxelplan
        self.view.open_kernels_configurator_callback = self.on_kernels_configuraotr
        self.view.add_new_plan_callback = self.on_add_new_plan
        self.view.about_callback = self.on_about
        self.view.trip_config_callback = self.on_trip98_config

        # view canvas
        self.model.one_plot_model = PlotModel()
        self.model.one_plot_cont = ViewCanvasCont(self.model.one_plot_model, self.view.get_viewcanvas_view())

        # patients tree module
        patient_tree_view = self.view.get_patient_tree_view()
        # patients tree module callbacks
        self.model.patient_tree_cont = TreeWidgetController(self.model.patients, patient_tree_view)
        self.model.patient_tree_cont.update_selected_item_callback = self.on_selected_item
        self.model.patient_tree_cont.context_menu.new_patient_callback = self.on_add_new_patient
        self.model.patient_tree_cont.context_menu.open_voxelplan_callback = self.on_open_voxelplan
        self.model.patient_tree_cont.context_menu.add_new_plan_callback = self.on_add_new_plan
        self.model.patient_tree_cont.context_menu.execute_plan_callback = self.on_execute_plan

    def on_selected_item(self, patient, item):
        self.model.current_patient = patient
        self.model.one_plot_cont.set_patient(self.model.current_patient)

    def on_add_new_patient(self):
        new_patient = PatientGui(self.model.kernels)
        self.model.patients.append(new_patient)
        return new_patient

    def on_open_voxelplan(self):
        path = self.view.browse_file_path("Open Voxelpan", "Voxelplan (*.hed)")
        filename, extension = os.path.splitext(path)

        if filename == "":
            return

        if self.model.current_patient:
            patient = self.model.current_patient
        else:
            patient = self.on_add_new_patient()
            self.model.patient_tree_cont.synchronize()

        patient.open_ctx(filename + ".ctx")  # Todo catch exceptions
        patient.open_vdx(filename + ".vdx")  # Todo catch exceptions

        self.model.patient_tree_cont.synchronize()
        self.model.one_plot_cont.set_patient(self.model.current_patient)

    def on_add_new_plan(self):
        if not self.model.current_patient:
            message = InfoMessages["addNewPatient"]
            self.view.show_info(message[0], message[1])
            return

        if not self.model.current_patient.ctx or not self.model.current_patient.vdx:
            message = InfoMessages["loadCtxVdx"]
            self.view.show_info(message[0], message[1])
            return

        if not self.model.kernels:
            message = InfoMessages["configureKernelList"]
            self.view.show_info(message[0], message[1])
            return

        self.model.current_patient.add_new_plan()
        self.model.patient_tree_cont.synchronize()

    def on_kernels_configuraotr(self):
        """
        Kernel dialog opened from window->settings->kernel
        """
        from pytripgui.kernel_vc import KernelController

        model = self.model.kernels
        view = self.view.get_kernel_config_view()

        controller = KernelController(model, view)
        controller.set_view_from_model()
        view.show()

        if controller.user_clicked_save:
            self.settings.save()

    def on_trip98_config(self):
        """
        Config menu opened from window->Settings->TRiP98 Config
        """
        logger.debug("TRiP config menu()")

        from pytripgui.config_vc import ConfigController

        view = self.view.get_trip_config_view()

        controller = ConfigController(self.model.executor.trip_config, view)
        controller.set_view_from_model()
        view.show()

        if controller.user_clicked_save:
            self.settings.save()

    def on_execute_plan(self, patient, plan):
        if not plan.fields:
            message = InfoMessages["addOneField"]
            self.view.show_info(message[0], message[1])
            return

        results = self.model.executor.execute(patient, plan)
        patient.simulation_results.append(results)

    def on_about(self):
        message = InfoMessages["about"]
        self.view.show_info(message[0], message[1])
