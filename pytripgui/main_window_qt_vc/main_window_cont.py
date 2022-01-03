import logging

from pytripgui.app_logic.viewcanvas import ViewCanvases
from pytripgui.loading_file_vc.loading_file_view import LoadingFileView
from pytripgui.messages import InfoMessages

from pytripgui.app_logic.patient_tree import PatientTree
from pytripgui.app_logic.app_callbacks import AppCallback
import sys
import os

from pytripgui.tree_vc.tree_items import PatientItem

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
        self.app_callback = AppCallback(self)

        self.model.patient_tree = PatientTree(self.view.ui)
        self.model.patient_tree.app_callback(self.app_callback)

        # main window callbacks
        self.view.open_voxelplan_callback = self.app_callback.on_open_voxelplan
        self.view.open_dicom_callback = self.app_callback.on_open_dicom
        self.view.import_dose_voxelplan_callback = self.app_callback.import_dose_voxelplan_callback
        self.view.import_dose_dicom_callback = self.app_callback.import_dose_dicom_callback
        # self.view.import_let_callback = self.app_callback.on_import_let
        self.view.open_kernels_configurator_callback = self.app_callback.on_kernels_configurator
        self.view.add_new_plan_callback = self.app_callback.on_add_new_plan
        self.view.trip_config_callback = self.app_callback.on_trip98_config
        self.view.action_add_patient = self.app_callback.on_add_patient
        self.view.action_add_vois = self.app_callback.on_add_vois
        self.view.action_create_field = self.app_callback.on_create_field
        self.view.action_execute_plan = self.app_callback.on_execute_selected_plan
        self.view.action_open_tree = self.app_callback.patient_tree_show

        self.view.about_callback = self.on_about
        self.view.exit_callback = self.on_exit

    def open_voxelplan(self, path):
        """
        Opens Voxelplan
        :param path: path to .hed file
        :return: True if voxelplan is opened, False otherwise
        """
        filename, _ = os.path.splitext(path)
        if not filename:
            return False

        patient = PatientItem()
        patient_data = patient.data
        try:
            patient_data.open_ctx(path)
        except FileNotFoundError as e:
            logger.error(str(e))
            return False
        try:
            patient_data.open_vdx(filename + ".vdx")  # Todo catch more exceptions
        except FileNotFoundError:
            logger.warning("Loaded patient has no VOI data")
            # TODO add empty vdx init if needed
            patient_data.vdx = None

        self._add_new_item(None, patient)
        return True

    def open_dicom(self, path):
        """
        Opens Dicom
        :param path: path to dicom directory
        :return: True if dicom is opened, False otherwise
        """
        if not path:
            return False

        patient = PatientItem()
        patient_data = patient.data
        patient_data.open_dicom(path)  # Todo catch exceptions

        self._add_new_item(None, patient)
        return True

    def _add_new_item(self, item_list_parent, item):
        if not self.model.viewcanvases:
            self.model.viewcanvases = ViewCanvases(self.view.ui)
            self.view.add_widget(self.model.viewcanvases.widget())

        self.model.patient_tree.add_new_item(item_list_parent, item)
        return True

    def on_about(self):
        """
        Callback to display the "about" box.
        """
        self.view.show_info(*InfoMessages["about"])

    @staticmethod
    def on_exit():
        sys.exit()
