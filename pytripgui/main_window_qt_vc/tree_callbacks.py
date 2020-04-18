from pytripgui.plan_vc.plan_view import PlanQtView
from pytripgui.plan_vc.plan_cont import PlanController
from pytripgui.field_vc.field_view import FieldQtView
from pytripgui.field_vc.field_cont import FieldController

from pytripgui.tree_vc.TreeItems import PatientItem
from pytripgui.tree_vc.TreeItems import PlanItem
from pytripgui.tree_vc.TreeItems import FieldItem

import logging
logger = logging.getLogger(__name__)


class TreeCallback:
    def __init__(self, global_kernels, parent_gui=None):
        self.kernels = global_kernels
        self.parent_gui = parent_gui

    def edit_item_callback(self, item, patient):
        if isinstance(item, PatientItem):
            return True
        elif isinstance(item, PlanItem):
            return self.edit_plan(item, patient)
        elif isinstance(item, FieldItem):
            return self.edit_field(item)

    def edit_plan(self, item, patient):
        logger.debug("edit_plan()".format())

        view = PlanQtView(self.parent_gui)

        controller = PlanController(item.data, view, self.kernels, patient.data.vdx.vois)
        controller.set_view_from_model()
        view.show()

        return controller.user_clicked_save

    def edit_field(self, item):
        logger.debug("edit_field()".format())

        view = FieldQtView()

        controller = FieldController(item.data, view, self.kernels)
        controller.set_view_from_model()
        view.show()

        return controller.user_clicked_save
