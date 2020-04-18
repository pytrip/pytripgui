import os
import logging

from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtCore import Qt

from pytripgui.controller.settings_cont import SettingsController
from pytripgui.tree_vc.TreeController import TreeController
from pytripgui.viewcanvas_vc.viewcanvas_cont import ViewCanvasCont
from pytripgui.messages import InfoMessages

from pytripgui.tree_vc.TreeView import TreeView

from pytripgui.main_window_qt_vc.tree_callbacks import TreeCallback

logger = logging.getLogger(__name__)


class MainWindowController(object):
    """
    TODO: some description here
    """
    def __init__(self, model, view):
        """
        TODO: some description here
        """
        self.model = model
        self.view = view

        self._initialize()

    def open_files(self, args):
        """
        TODO: some description here
        """
        pass
        # raise Exception("Unimplemented")  # TODO

    def _initialize(self):
        """
        TODO: some description here
        """
        self.settings = SettingsController(self.model)

        # main window callbacks
        self.view.open_voxelplan_callback = self.on_open_voxelplan
        self.view.open_kernels_configurator_callback = self.on_kernels_configurator
        self.view.add_new_plan_callback = self.on_add_new_plan
        self.view.about_callback = self.on_about
        self.view.trip_config_callback = self.on_trip98_config

        self.view.one_viewcanvas_view = self.view.get_viewcanvas_view()
        self.model.one_plot_cont = ViewCanvasCont(None, self.view.one_viewcanvas_view)

        # patients tree module
        self.model.patient_tree_view = TreeView()
        self.model.patient_tree_view.setModel(self.model.patient_tree_model)
        self.model.patient_tree_cont = TreeController(self.model.patient_tree_model, self.model.patient_tree_view)
        self.tree_callback = TreeCallback(self.model.kernels, self.view.ui)
        self.model.patient_tree_cont.edit_item_callback = self.tree_callback.edit_item_callback
        self.model.patient_tree_cont.open_voxelplan_callback = self.on_open_voxelplan

        widget = QDockWidget()
        widget.setWidget(self.model.patient_tree_view)
        self.view.ui.addDockWidget(Qt.LeftDockWidgetArea, widget)

    def on_selected_item(self, patient, item):
        """
        TODO: some description here
        """
        self.model.current_patient = patient
        self.model.one_plot_cont.set_patient(patient)

    def on_open_voxelplan(self, patient_item):
        """
        TODO: some description here
        """
        path = self.view.browse_file_path("Open Voxelpan", "Voxelplan (*.hed)")
        filename, extension = os.path.splitext(path)

        if filename == "":
            return

        patient = patient_item.data
        patient.open_ctx(filename + ".ctx")  # Todo catch exceptions
        patient.open_vdx(filename + ".vdx")  # Todo catch exceptions

        self.model.one_plot_cont.set_patient(patient)

    def on_add_new_plan(self, patient):
        """
        TODO: some description here
        """
        if not patient.ctx or not patient.vdx:
            self.view.show_info(*InfoMessages["loadCtxVdx"])
            return False

        if not self.model.kernels:
            self.view.show_info(*InfoMessages["configureKernelList"])
            return False

        self.model.current_patient.add_new_plan()
        self.model.patient_tree_cont.synchronize()

    def on_kernels_configurator(self):
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
        """
        TODO: some description here
        """
        if not plan.fields:
            self.view.show_info(*InfoMessages["addOneField"])
            return

        if self.model.executor.check_config() != 0:
            self.view.show_info(*InfoMessages["configureTrip"])
            return

        if not plan.kernel.sis_path:
            self.view.show_info(*InfoMessages["kernelSisPath"])
            return

        results = self.model.executor.execute(patient, plan)
        patient.simulation_results.append(results)
        self.model.one_plot_cont.set_patient(self.model.current_patient)

    def on_about(self):
        """
        Callback to display the "about" box.
        """
        self.view.show_info(*InfoMessages["about"])
