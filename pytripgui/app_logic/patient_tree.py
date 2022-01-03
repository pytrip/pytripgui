import logging

from pytripgui.tree_vc.tree_model import TreeModel
from pytripgui.tree_vc.tree_items import PatientList

from pytripgui.tree_vc.tree_controller import TreeController
from pytripgui.tree_vc.tree_view import TreeView

logger = logging.getLogger(__name__)


class PatientTree:
    def __init__(self, parent):
        self.patient_tree_model = TreeModel(PatientList())
        self.patient_tree_view = TreeView()

        self.patient_tree_view.setModel(self.patient_tree_model)
        self.patient_tree_cont = TreeController(self.patient_tree_model, self.patient_tree_view)

        self._parent = parent

        self.widget = self._parent.patientTree_dockWidget
        self.widget.setWidget(self.patient_tree_view)

    def set_visible(self, visible):
        if visible:
            self.widget.show()
        else:
            self.widget.hide()

    def app_callback(self, app_callback):
        self.patient_tree_cont.new_item_callback = app_callback.new_item_callback
        self.patient_tree_cont.edit_item_callback = app_callback.edit_item_callback

        self.patient_tree_cont.open_voxelplan_callback = app_callback.on_open_voxelplan
        self.patient_tree_cont.open_dicom_callback = app_callback.on_open_dicom

        self.patient_tree_cont.export_patient_voxelplan_callback = app_callback.export_patient_voxelplan_callback
        self.patient_tree_cont.export_patient_dicom_callback = app_callback.export_patient_dicom_callback
        self.patient_tree_cont.export_dose_voxelplan_callback = app_callback.export_dose_voxelplan_callback
        self.patient_tree_cont.export_dose_dicom_callback = app_callback.export_dose_dicom_callback
        self.patient_tree_cont.export_plan_callback = app_callback.export_plan_exec_callback

        self.patient_tree_cont.import_dose_voxelplan_callback = app_callback.import_dose_voxelplan_callback
        self.patient_tree_cont.import_dose_dicom_callback = app_callback.import_dose_dicom_callback

        self.patient_tree_cont.execute_plan_callback = app_callback.on_execute_selected_plan
        self.patient_tree_cont.one_click_callback = app_callback.one_click_callback

    def add_new_item(self, parent_item, item):
        self.patient_tree_cont.add_new_item(parent_item, item)

    def selected_item_patient(self):
        return self.patient_tree_view.selected_item_patient

    def selected_item(self):
        return self.patient_tree_view.selected_item
