import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeView

logger = logging.getLogger(__name__)


class TreeView(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.clicked_callback = None
        self.context_menu_callback = None

    def set_item_clicked_callback(self, fun):
        self.clicked_callback = fun
        # self._ui.itemClicked.connect(self._internal_item_clicked_callback)  # todo

    def _internal_item_clicked_callback(self, item_clicked, pos):
        clicked_item_content = item_clicked.data(0, Qt.UserRole)

        patient_clicked = item_clicked
        while patient_clicked.parent():
            patient_clicked = patient_clicked.parent()
        patient_clicked_content = patient_clicked.data(0, Qt.UserRole)

        self.clicked_callback(patient_clicked_content, clicked_item_content)

    def set_custom_context_menu(self, fun):
        self.context_menu_callback = fun
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._internal_context_menu_callback)

    def _internal_context_menu_callback(self, pos):
        # item_clicked = self._ui.selectedItems()
        # if item_clicked:
        #     clicked_item_content = item_clicked[0].data(0, Qt.UserRole)
        #
        #     patient_clicked = item_clicked[0]
        #     while patient_clicked.parent():
        #         patient_clicked = patient_clicked.parent()
        #     patient_clicked_content = patient_clicked.data(0, Qt.UserRole)
        # else:
        clicked_item_content = None
        patient_clicked_content = None

        self.context_menu_callback(patient_clicked_content, clicked_item_content, pos)
