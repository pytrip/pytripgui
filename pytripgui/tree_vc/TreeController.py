import logging

from pytripgui.tree_vc.TreeItems import PatientItem
from pytripgui.tree_vc.TreeItems import PlanItem

from pytripgui.plan_vc import PlanQtView
from pytripgui.plan_vc import PlanController

logger = logging.getLogger(__name__)


class TreeController:
    def __init__(self, model, view, kernel_list=None):
        self._tree_model = model
        self._view = view
        self._view.add_child_callback = self.add_new_item
        self._kernel_list = kernel_list

        self.add_child_callback = None

    def add_new_item(self, parent=None):
        if self.add_child_callback:
            if parent:
                data = parent.internalPointer()
            else:
                data = None
            child = self.add_child_callback(data)

            if not child:
                return
        else:
            logger.warning("You have not set add_new_item_callback")

        self._tree_model.insertRows(0, 1, parent)

    def add_new_patient(self):
        patient = PatientItem()
        self._tree_model.add_patient(patient)

        logger.debug("add_new_plan() {}".format(None))

    def add_new_plan(self):
        plan = PlanItem()

        view = PlanQtView()
        plan.data.kernel = None
        controller = PlanController(plan.data, view, self._kernel_list, [])
        controller.set_view_from_model()
        view.show()

        if controller.user_clicked_save:
            self.plans.append(plan)

        self._view.selected_patient.add_child(plan)
