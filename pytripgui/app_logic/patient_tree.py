import logging

from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtCore import Qt

from pytripgui.tree_vc.tree_model import TreeModel
from pytripgui.tree_vc.tree_items import PatientList

from pytripgui.tree_vc.tree_controller import TreeController
from pytripgui.tree_vc.tree_view import TreeView

logger = logging.getLogger(__name__)


class PatientTree:
    def __init__(self, gui, parent_view):
        self._gui = gui
        self.patient_tree_model = TreeModel(PatientList())
        self.patient_tree_view = TreeView()

        self.patient_tree_view.setModel(self.patient_tree_model)
        self.patient_tree_cont = TreeController(self.patient_tree_model, self.patient_tree_view)

        self.patient_tree_view.internal_events.on_export_voxelplan = self._export_cube_callback
        self._parent_view = parent_view

        self.widget = QDockWidget()
        self.widget.setFeatures(self.widget.features() & ~QDockWidget.DockWidgetClosable)
        self.widget.setWidget(self.patient_tree_view)
        self._parent_view.addDockWidget(Qt.LeftDockWidgetArea, self.widget)
        self.widget.setWindowTitle("Patient tree")

    def set_visible(self, visible):
        if visible:
            self.widget.show()
        else:
            self.widget.hide()

    def app_callback(self, app_callback):
        self.patient_tree_cont.new_item_callback = app_callback.new_item_callback
        self.patient_tree_cont.edit_item_callback = app_callback.edit_item_callback
        self.patient_tree_cont.open_voxelplan_callback = app_callback.open_voxelplan_callback
        self.patient_tree_cont.open_dicom_callback = app_callback.open_dicom_callback
        self.patient_tree_cont.export_patient_voxelplan_callback = app_callback.export_patient_voxelplan_callback
        self.patient_tree_cont.export_patient_dicom_callback = app_callback.export_patient_dicom_callback
        self.patient_tree_cont.execute_plan_callback = app_callback.on_execute_selected_plan
        self.patient_tree_cont.one_click_callback = app_callback.one_click_callback

    def add_new_item(self, parent_item, item):
        self.patient_tree_cont.add_new_item(parent_item, item)

    def selected_item_patient(self):
        return self.patient_tree_view.selected_item_patient

    def selected_item(self):
        return self.patient_tree_view.selected_item

    def _export_cube_callback(self):
        item = self.selected_item()
        path = self._gui.browse_folder_path("Select output directory")
        if path:
            path += item.data.basename
            item.data.write(path)
