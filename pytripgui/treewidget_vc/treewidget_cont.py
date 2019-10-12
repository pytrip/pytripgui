import logging

from pytripgui.treewidget_vc.treewidget_context_menu import TreeWidgetContextMenu

logger = logging.getLogger(__name__)


class TreeWidgetController:
    def __init__(self, model, view):
        self._patients = model
        self._view = view
        self.context_menu = TreeWidgetContextMenu(self)

        self.synchronize()

        self._view.set_item_clicked_callback(self._clicked_item_callback)
        self.update_selected_item_callback = None

        self._view.set_custom_context_menu(self.context_menu.custom_context_menu_callback)

    def synchronize(self):
        for patient in self._patients:
            self.add_patient_tree(patient)
            self.synchronize_ctx(patient)
            self.synchronize_vdx(patient)
            self.synchronize_plans(patient)
            self.synchronize_simulation_results(patient)

    def _clicked_item_callback(self, clicked_patient, clicked_item):
        self._view.set_header_label("Patient: " + clicked_patient.name)
        if self.update_selected_item_callback:
            self.update_selected_item_callback(clicked_patient, clicked_item)

    def add_patient_tree(self, patient):
        if patient.tree_model.patient_tree is None:
            patient_tree = self._view.add_tree(patient, patient.name)
            patient.tree_model.patient_tree = patient_tree
        else:
            self._view.set_data_in_sub_item(
                patient.tree_model.patient_tree,
                patient,
                patient.name)

    def synchronize_ctx(self, patient):
        item = patient.ctx
        if item:
            item_name = "ctx: " + item.basename
            item_tree = patient.tree_model.ctx_tree
            patient_tree = patient.tree_model.patient_tree

            if item_tree is None:
                patient.tree_model.ctx_tree = self._view.add_sub_item(
                    patient_tree,
                    item,
                    item_name)
            else:
                self._view.set_data_in_sub_item(item_tree, item, item_name)

    def synchronize_vdx(self, patient):
        item = patient.vdx
        if item:
            item_name = "vdx: " + item.basename
            item_tree = patient.tree_model.vdx_tree
            patient_tree = patient.tree_model.patient_tree

            if item_tree is None:
                patient.tree_model.vdx_tree = self._view.add_sub_item(
                    patient_tree,
                    item,
                    item_name)
            else:
                self._view.set_data_in_sub_item(item_tree, item, item_name)

    def synchronize_plans(self, patient):
        item = patient.plans
        if item:
            item_name = "Plans:"
            item_tree = patient.tree_model.plans_tree
            patient_tree = patient.tree_model.patient_tree

            if item_tree is None:
                patient.tree_model.plans_tree = self._view.add_sub_item(
                    patient_tree,
                    item,
                    item_name)
            else:
                self._view.set_data_in_sub_item(item_tree, item, item_name)

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

    def synchronize_simulation_results(self, patient):
        item = patient.simulation_results
        if item:
            item_name = "Simulation results:"
            item_tree = patient.tree_model.simulations_tree
            patient_tree = patient.tree_model.patient_tree

            if item_tree is None:
                patient.tree_model.simulations_tree = self._view.add_sub_item(
                    patient_tree,
                    item,
                    item_name)
            else:
                self._view.set_data_in_sub_item(item_tree, item, item_name)

            self._view.clear_tree(patient.tree_model.simulations_tree)

            for simulation in patient.simulation_results:
                self.add_simulation_results(patient, simulation)

    def add_simulation_results(self, patient, simulation):
        simulations_tree = patient.tree_model.simulations_tree

        # Add current simulation
        current_simulation_tree = self._view.add_sub_item(
            simulations_tree,
            simulation,
            simulation.name)

        # Add old plan snapshot to simulation
        self._view.add_sub_item(
            current_simulation_tree,
            simulation.plan_snapshot,
            "Plan snapshot: " + simulation.name)

        if simulation.dos:
            self._view.add_sub_item(
                current_simulation_tree,
                simulation.dos,
                "Dos")

        if simulation.let:
            self._view.add_sub_item(
                current_simulation_tree,
                simulation.let,
                "Let")

        # for field in plan.fields:
        #     self.add_field_to_plan_tree(plan_tree, field)
