import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeView

from PyQt5.QtWidgets import QMenu
from PyQt5.QtCore import QPoint

from pytripgui.tree_vc.TreeItems import PatientItem
from pytripgui.tree_vc.TreeItems import PlanItem

logger = logging.getLogger(__name__)


class TreeView(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.selected_patient = None
        self.selected_q_item = None
        self.selected_item = None

        self.context_menu = None

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._internal_context_menu_callback)

        self.add_child_callback = None
        self.edit_item_callback = None

    def _internal_context_menu_callback(self, pos):
        self._update_selected_item()

        popup_menu = QMenu(self)

        if self.selected_item is None:
            popup_menu.addAction("Add new Patient", self._add_child)
        elif isinstance(self.selected_item, PatientItem):
            popup_menu.addAction("Add new Plan", self._add_child)
            popup_menu.addSeparator()
        elif isinstance(self.selected_item, PlanItem):
            popup_menu.addAction("Add new Field", self._add_child)
        else:
            return

        menu_position = pos + QPoint(10, 10)
        node = self.mapToGlobal(menu_position)
        popup_menu.exec_(node)

    def _update_selected_item(self):
        """
        this method updates following fields:
            self.selected_patient
            self.selected_item
        based on item selected by user in TreeView.
        :return:
        """
        selected_item = self.selectedIndexes()

        if selected_item:
            self.selected_q_item = selected_item[0]
            self.selected_item = selected_item[0].internalPointer()

            patient_clicked = selected_item[0]
            while patient_clicked.parent().parent().isValid():
                patient_clicked = patient_clicked.parent()

            self.selected_patient = patient_clicked

    def _add_child(self):
        if self.add_child_callback:
            self.add_child_callback(self.selected_q_item)
