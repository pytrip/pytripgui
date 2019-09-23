from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItem

import logging
logger = logging.getLogger(__name__)


class TreeWidgetView:
    def __init__(self, ui):
        self._ui = ui
        self.clicked_callback = None

    def add_new_patient(self, patient):
        patient_tree = QTreeWidgetItem([patient.name])
        patient_tree.setData(0, Qt.UserRole, patient)

        patient.tree_model.patient_tree = patient_tree
        self._ui.addTopLevelItem(patient_tree)
        self._ui.expandItem(patient_tree)
        return patient_tree

    @staticmethod
    def add_ctx_to_patient(patient, ctx):
        ctx_hook = QTreeWidgetItem(["ctx: " + ctx.basename])
        ctx_hook.setData(0, Qt.UserRole, ctx)
        patient.tree_model.patient_tree.addChild(ctx_hook)
        patient.tree_model.ctx_tree = ctx_hook

    @staticmethod
    def add_vdx_to_patient(patient, vdx):
        vdx_hook = QTreeWidgetItem(["vdx: " + vdx.basename])
        vdx_hook.setData(0, Qt.UserRole, vdx)
        patient.tree_model.patient_tree.addChild(vdx_hook)
        patient.tree_model.vdx_tree = vdx_hook

    @staticmethod
    def add_plans_to_patient(patient, plans):
        plans_hook = QTreeWidgetItem(["Plans:"])
        plans_hook.setData(0, Qt.UserRole, plans)
        patient.tree_model.plans_tree = plans_hook
        patient.tree_model.patient_tree.addChild(plans_hook)

        for plan in plans:
            plan_hook = QTreeWidgetItem(["plan"])
            plan_hook.setData(0, Qt.UserRole, plan)
            patient.tree_model.plans_tree.addChild(plan_hook)

    def set_header_label(self, label):
        self._ui.setHeaderLabels([label])

    def clear(self):
        self._ui.clear()

    def set_item_clicked_callback(self, fun):
        self.clicked_callback = fun
        self._ui.itemClicked.connect(self._internal_item_clicked_callback)

    def _internal_item_clicked_callback(self, item, pos):
        item_clicked = item.data(0, Qt.UserRole)
        self.clicked_callback(item_clicked, 1)
