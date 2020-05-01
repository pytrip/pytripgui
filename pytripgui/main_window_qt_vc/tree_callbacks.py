from pytripgui.plan_vc.plan_view import PlanQtView
from pytripgui.plan_vc.plan_cont import PlanController
from pytripgui.field_vc.field_view import FieldQtView
from pytripgui.field_vc.field_cont import FieldController

from pytripgui.tree_vc.TreeItems import PatientItem
from pytripgui.tree_vc.TreeItems import PlanItem
from pytripgui.tree_vc.TreeItems import FieldItem

from pytripgui.messages import InfoMessages

import os

import logging
logger = logging.getLogger(__name__)


class TreeCallback:
    def __init__(self, global_data, executor=None, parent_gui=None):
        self.global_data = global_data
        self.parent_gui = parent_gui
        self.executor = executor

    def edit_item_callback(self, item, patient):
        if isinstance(item, PatientItem):
            return True
        elif isinstance(item, PlanItem):
            return self.edit_plan(item, patient)
        elif isinstance(item, FieldItem):
            return self.edit_field(item)

    def edit_plan(self, item, patient):
        logger.debug("edit_plan()".format())

        if not patient.data.vdx:
            self.parent_gui.show_info(*InfoMessages["loadCtxVdx"])
            return False

        item.data.basename = patient.data.name

        view = PlanQtView(self.parent_gui.ui)

        controller = PlanController(item.data, view, self.global_data.kernels, patient.data.vdx.vois)
        controller.set_view_from_model()
        view.show()

        return controller.user_clicked_save

    def edit_field(self, item):
        logger.debug("edit_field()".format())

        view = FieldQtView(self.parent_gui.ui)

        item.data.basename = "field"
        controller = FieldController(item.data, view, self.global_data.kernels)
        controller.set_view_from_model()
        view.show()

        return controller.user_clicked_save

    def execute_plan(self, plan, patient):
        if plan.children:
            plan.data.fields.append(plan.children[0].data)
        else:
            self.parent_gui.show_info(*InfoMessages["addOneField"])
            return
        self.executor.execute(patient.data, plan.data)

    def open_voxelplan_callback(self, patient_item):
        path = self.parent_gui.browse_file_path("Open Voxelpan", "Voxelplan (*.hed)")
        filename, extension = os.path.splitext(path)

        if filename == "":
            return

        patient = patient_item.data
        patient.open_ctx(filename + ".ctx")  # Todo catch exceptions
        patient.open_vdx(filename + ".vdx")  # Todo catch exceptions

        self.global_data.one_plot_cont.set_patient(patient)
