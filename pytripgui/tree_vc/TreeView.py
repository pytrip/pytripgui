import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeView

logger = logging.getLogger(__name__)


class TreeView(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.selected_patient = None
        self.selected_item = None

        self.context_menu = None

    def set_custom_context_menu(self, context_menu):
        self.context_menu = context_menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._internal_context_menu_callback)

    def _internal_context_menu_callback(self, pos):
        self._update_selected_item()
        self.context_menu.callback(self.selected_item, pos)

    def _update_selected_item(self):
        selected_item = self.selectedIndexes()

        if selected_item:
            self.selected_item = selected_item[0].internalPointer()

            patient_clicked = selected_item[0]
            while patient_clicked.parent().parent().isValid():
                patient_clicked = patient_clicked.parent()

            self.selected_patient = patient_clicked.internalPointer()

