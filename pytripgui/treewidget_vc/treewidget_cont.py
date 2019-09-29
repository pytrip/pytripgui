from pytripgui.treewidget_vc.treewidget_context_menu import TreeWidgetContextMenu

import logging
logger = logging.getLogger(__name__)


class TreeWidgetController:
    def __init__(self, model, view):
        self._patients = model
        self._view = view
        self._context_menu = TreeWidgetContextMenu(self)

        self.synchronize()
        self.synchronize()
        self._view.set_item_clicked_callback(self.non)
        self._view.set_custom_context_menu(self._context_menu.custom_context_menu_callback)

    def synchronize(self):
        for patient in self._patients:
            self.add_patient_tree(patient)
            self.synchronize_ctx(patient)
            self.synchronize_vdx(patient)
            self.synchronize_plans(patient)

            # if patient.plans:
            #     self._view.add_plans_to_patient(patient, patient.plans)
            #
            # self._model.patient_tree = patient_tree

    def non(self, xd, zz):
        pass

    def add_patient_tree(self, patient):
        if patient.tree_model.patient_tree is None:
            patient_tree = self._view.add_tree(patient, patient.name)
            patient.tree_model.patient_tree = patient_tree

    def synchronize_ctx(self, patient):
        item = patient.ctx
        item_name = "ctx: " + item.basename
        item_tree = patient.tree_model.ctx_tree
        patient_tree = patient.tree_model.patient_tree

        if item:
            if item_tree is None:
                patient.tree_model.ctx_tree = self._view.add_sub_item(
                    patient_tree,
                    item,
                    item_name)
            else:
                self._view.exchange_data_in_sub_item(item_tree, item, item_name)

    def synchronize_vdx(self, patient):
        item = patient.vdx
        item_name = "vdx: " + item.basename
        item_tree = patient.tree_model.vdx_tree
        patient_tree = patient.tree_model.patient_tree

        if item:
            if item_tree is None:
                patient.tree_model.vdx_tree = self._view.add_sub_item(
                    patient_tree,
                    item,
                    item_name)
            else:
                self._view.exchange_data_in_sub_item(item_tree, item, item_name)

    def synchronize_plans(self, patient):
        item = patient.plans
        item_name = "Plans:"
        item_tree = patient.tree_model.plans_tree
        patient_tree = patient.tree_model.patient_tree

        if item:
            if item_tree is None:
                patient.tree_model.plans_tree = self._view.add_sub_item(
                    patient_tree,
                    item,
                    item_name)
            else:
                self._view.exchange_data_in_sub_item(item_tree, item, item_name)

            self._view.clear_tree(patient.tree_model.plans_tree)

            for plan in patient.plans:
                self.add_plan(patient, plan)

    def add_plan(self, patient, plan):
        plans_tree = patient.tree_model.plans_tree

        plan_tree = self._view.add_sub_item(
            plans_tree,
            plan,
            plan.basename)

        for field in plan.fields:
            self.add_field_to_plan_tree(plan_tree, field)

    def add_field_to_plan_tree(self, plan_tree, field):
        self._view.add_sub_item(
            plan_tree,
            field,
            field.basename)
