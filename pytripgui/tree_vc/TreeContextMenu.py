import logging

from PyQt5.QtWidgets import QMenu
from PyQt5.QtCore import QPoint

from pytripgui.tree_vc.TreeItems import PatientItem
from pytripgui.tree_vc.TreeItems import PlanItem

logger = logging.getLogger(__name__)


class TreeContextMenu:
    def __init__(self, parent_view, tree_cont):
        self._parent_view = parent_view
        self._tree_controller = tree_cont

    def callback(self, item, pos):
        """
        This function is called after user click right mouse button on TreeView
        :param item:
        :param pos:
        :return:
        """
        popup_menu = QMenu(self._parent_view)

        if item is None:
            popup_menu.addAction("Add new Patient", self._tree_controller.add_new_patient)
        elif isinstance(item, PatientItem):
            popup_menu.addAction("Add new Plan", self._tree_controller.add_new_plan)
            popup_menu.addSeparator()
        elif isinstance(item, PlanItem):
            popup_menu.addAction("Add new Plan", self._tree_controller.add_new_plan)
        else:
            return

        menu_position = pos + QPoint(10, 10)
        node = self._parent_view.mapToGlobal(menu_position)
        popup_menu.exec_(node)
