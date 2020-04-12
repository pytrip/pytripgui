import logging
logger = logging.getLogger(__name__)

from pytripgui.plan_vc.plan_view import PlanQtView
from pytripgui.plan_vc.plan_cont import PlanController
from pytripgui.field_vc.field_view import FieldQtView
from pytripgui.field_vc.field_cont import FieldController

from pytripgui.tree_vc.TreeItems import PatientItem
from pytripgui.tree_vc.TreeItems import PlanItem
from pytripgui.tree_vc.TreeItems import FieldItem


def edit_item_callback(item):
    if isinstance(item, PatientItem):
        return True
    elif isinstance(item, PlanItem):
        return edit_plan(item)
    elif isinstance(item, FieldItem):
        return edit_field(item)


def edit_plan(item):
    logger.debug("edit_plan()".format())

    view = PlanQtView()

    controller = PlanController(item.data, view, [], [])
    controller.set_view_from_model()
    view.show()

    return controller.user_clicked_save


def edit_field(item):
    logger.debug("edit_field()".format())

    view = FieldQtView()

    controller = FieldController(item.data, view, [])
    controller.set_view_from_model()
    view.show()

    return controller.user_clicked_save
