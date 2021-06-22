import logging

from pytripgui.messages import InfoMessages

from pytripgui.app_logic.patient_tree import PatientTree
from pytripgui.app_logic.app_callbacks import AppCallback
import sys

logger = logging.getLogger(__name__)


class MainWindowController:
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

    def _initialize(self):
        """
        TODO: some description here
        """
        self.app_callback = AppCallback(self.model, self.view)

        self.model.patient_tree = PatientTree(self.view, self.view.ui)
        self.model.patient_tree.app_callback(self.app_callback)

        # main window callbacks
        self.view.open_voxelplan_callback = self.app_callback.on_open_voxelplan
        self.view.open_dicom_callback = self.app_callback.on_open_dicom
        self.view.open_kernels_configurator_callback = self.app_callback.on_kernels_configurator
        self.view.add_new_plan_callback = self.app_callback.on_add_new_plan
        self.view.trip_config_callback = self.app_callback.on_trip98_config
        self.view.action_add_patient = self.app_callback.on_add_patient
        self.view.action_create_field = self.app_callback.on_create_field
        self.view.action_execute_plan = self.app_callback.on_execute_selected_plan
        self.view.action_open_tree = self.app_callback.patient_tree_show

        self.view.about_callback = self.on_about
        self.view.exit_callback = self.on_exit

    def on_about(self):
        """
        Callback to display the "about" box.
        """
        self.view.show_info(*InfoMessages["about"])

    @staticmethod
    def on_exit():
        sys.exit()
