import logging
from events import Events

from PyQt5.QtCore import Qt, QPoint, QModelIndex
from PyQt5.QtWidgets import QTreeView, QMenu

from pytripgui.tree_vc.TreeItems import PatientItem
from pytripgui.tree_vc.TreeItems import PlanItem
from pytripgui.tree_vc.TreeItems import FieldItem

logger = logging.getLogger(__name__)


class TreeView(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.selected_q_item = QModelIndex()

        self.selected_item = None
        self.selected_item_patient = None   # patient to which selected_item belongs

        """
        Those events should only be subscribed only by TreeController
        """
        self.internal_events = Events((
            'on_add_child',
            'on_edit_selected_item',
            'on_open_voxelplan',
            'on_open_dicom'
        ))

        self._init_q_tree_view()

    def _init_q_tree_view(self):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._internal_context_menu_callback)
        self.clicked.connect(self._update_selected_item)

    def _internal_context_menu_callback(self, pos):
        self._update_selected_item()

        popup_menu = QMenu(self)

        if self.selected_item is None:
            popup_menu.addAction("Add new Patient", self.internal_events.on_add_child)
        elif isinstance(self.selected_item, PatientItem):
            popup_menu.addAction("Open Voxelplan", self.internal_events.on_open_voxelplan)
            popup_menu.addAction("Add new Plan", self.internal_events.on_add_child)
        elif isinstance(self.selected_item, PlanItem):
            popup_menu.addAction("Add new Field", self.internal_events.on_add_child)
            popup_menu.addSeparator()
            popup_menu.addAction("Edit selected Plan", self.internal_events.on_edit_selected_item)
        elif isinstance(self.selected_item, FieldItem):
            popup_menu.addAction("Edit selected Field", self.internal_events.on_edit_selected_item)
        else:
            return

        menu_position = pos + QPoint(10, 10)
        node = self.mapToGlobal(menu_position)
        popup_menu.exec_(node)

    def _update_selected_item(self, q_index=None):
        """
        this method updates following fields:
            self.selected_q_item
            self.selected_item
            self.selected_item_patient
        based on item selected in TreeView.
        :return:
        """
        if q_index:
            selected_item = q_index
        else:
            selected_item = self.selectedIndexes()
            if selected_item:
                selected_item = selected_item[0]

        if selected_item:
            self.selected_q_item = selected_item
            self.selected_item = selected_item.internalPointer()

            patient_clicked = selected_item
            while patient_clicked.parent().parent().isValid():
                patient_clicked = patient_clicked.parent()

            self.selected_patient = patient_clicked
