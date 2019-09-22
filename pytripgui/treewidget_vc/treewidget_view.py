from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItem

import logging
logger = logging.getLogger(__name__)


class TreeWidgetView:
    def __init__(self, ui):
        self._ui = ui

    def init_widget(self, tree_model):
        tree_model.patient_tree = QTreeWidgetItem(["Patient Name"])
        self._ui.addTopLevelItem(tree_model.patient_tree)

        tree_model.ctx_tree = QTreeWidgetItem(["CTX"])
        tree_model.patient_tree.addChild(tree_model.ctx_tree)

        tree_model.vdx_tree = QTreeWidgetItem(["VDX"])
        tree_model.patient_tree.addChild(tree_model.vdx_tree)

        tree_model.plans_tree = QTreeWidgetItem(["Plans"])
        tree_model.patient_tree.addChild(tree_model.plans_tree)

        tree_model.simulations_tree = QTreeWidgetItem(["Simulations"])
        tree_model.patient_tree.addChild(tree_model.simulations_tree)

    def add_new_patient(self, patient):
        new_item = QTreeWidgetItem([patient.name])
        new_item.setData(0, Qt.UserRole, patient)

        self._ui.addTopLevelItem(new_item)
        return new_item

    def add_ctx_to_patient(self, patient, ctx):
        ctx_hook = QTreeWidgetItem([patient.name])
        ctx_hook.setData(0, Qt.UserRole, patient)
        patient.addChild(ctx_hook)

    def set_header_label(self, label):
        self._ui.setHeaderLabels([label])
