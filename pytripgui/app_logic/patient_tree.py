import logging

from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtCore import Qt

from pytripgui.tree_vc.TreeModel import TreeModel
from pytripgui.tree_vc.TreeItems import PatientList

from pytripgui.tree_vc.TreeController import TreeController
from pytripgui.tree_vc.TreeView import TreeView

logger = logging.getLogger(__name__)


class PatientTree:
    def __init__(self):
        self.patient_tree_model = TreeModel(PatientList())
        self.patient_tree_view = TreeView()

        self.patient_tree_view.setModel(self.patient_tree_model)
        self.patient_tree_cont = TreeController(self.patient_tree_model, self.patient_tree_view)

    def show(self, parent_view):
        widget = QDockWidget()
        widget.setWidget(self.patient_tree_view)
        parent_view.addDockWidget(Qt.LeftDockWidgetArea, widget)

    def app_callback(self, app_callback):
        self.patient_tree_cont.new_item_callback = app_callback.new_item_callback
        self.patient_tree_cont.edit_item_callback = app_callback.edit_item_callback
        self.patient_tree_cont.open_voxelplan_callback = app_callback.open_voxelplan_callback
        self.patient_tree_cont.execute_plan_callback = app_callback.execute_plan
        self.patient_tree_cont.one_click_callback = app_callback.one_click_callback

    def add_new_item(self, parent_item, item):
        self.patient_tree_cont.add_new_item(parent_item, item)

    def selected_item_patient(self):
        return self.patient_tree_view.selected_item_patient

    def selected_item(self):
        return self.patient_tree_view.selected_item
