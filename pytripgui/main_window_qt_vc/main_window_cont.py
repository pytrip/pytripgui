import logging

from pytripgui.controller.settings_cont import SettingsController
from pytripgui.messages import InfoMessages
from pytripgui.view.qt_gui import UiAddPatient

from pytripgui.app_logic.patient_tree import PatientTree
from pytripgui.app_logic.app_callbacks import AppCallback

from pytripgui.tree_vc.TreeItems import PatientItem, PlanItem, FieldItem

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
        self.view.exit_callback = self.on_exit
        self.view.action_add_patient = self.on_add_patient
        self.view.action_create_field = self.on_create_field

        self.app_callback = AppCallback(self.model, self.model.executor, self.view)

        self.patient_tree = PatientTree(self.view)
        self.patient_tree.app_callback(self.app_callback)

        self.patient_tree.show(self.view.ui)

    def on_open_voxelplan(self):
        patient = PatientItem()
        if self.app_callback.open_voxelplan_callback(patient):
            self.patient_tree.add_new_item(None, patient)

    def on_add_new_plan(self):
        selected_patient = self.patient_tree.selected_item_patient()
        if not selected_patient:
            self.view.show_info(*InfoMessages["addNewPatient"])
            return
        plan = self.app_callback.new_item_callback(selected_patient)
        self.patient_tree.add_new_item(selected_patient, plan)

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

    def on_about(self):
        """
        Callback to display the "about" box.
        """
        self.view.show_info(*InfoMessages["about"])

    @staticmethod
    def on_exit():
        exit()

    def on_add_patient(self):
        dialog = UiAddPatient(self.view.ui)
        dialog.on_create_empty = self.add_empty_patient
        dialog.on_open_voxelplan = self.on_open_voxelplan
        dialog.show()

    def add_empty_patient(self):
        patient = PatientItem()
        self.patient_tree.add_new_item(None, patient)

    def on_create_field(self):
        field = FieldItem()
        save_field = self.app_callback.edit_field(field)
        if save_field:
            selected_item = self.patient_tree.selected_item()
            if isinstance(selected_item, PlanItem):
                selected_plan = selected_item
            elif isinstance(selected_item, FieldItem):
                selected_plan = selected_item.parent
            self.patient_tree.add_new_item(selected_plan, field)
