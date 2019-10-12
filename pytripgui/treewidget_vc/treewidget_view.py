import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItem

logger = logging.getLogger(__name__)


class TreeWidgetView:
    def __init__(self, ui):
        self._ui = ui
        self.clicked_callback = None
        self.context_menu_callback = None

    def add_tree(self, item, name):
        item_tree = QTreeWidgetItem([name])
        item_tree.setData(0, Qt.UserRole, item)

        self._ui.addTopLevelItem(item_tree)
        self._ui.expandItem(item_tree)
        if not self._ui.selectedItems():
            item_tree.setSelected(True)
            self.clicked_callback(item, item)

        return item_tree

    @staticmethod
    def add_sub_item(tree, item, name):
        item_hook = QTreeWidgetItem([name])
        item_hook.setData(0, Qt.UserRole, item)
        tree.addChild(item_hook)
        return item_hook

    @staticmethod
    def clear_tree(tree):
        tree.takeChildren()

    @staticmethod
    def set_data_in_sub_item(sub_item, item, name):
        sub_item.setData(0, Qt.UserRole, item)
        sub_item.setText(0, name)

    def set_header_label(self, label):
        self._ui.setHeaderLabels([label])

    def set_item_clicked_callback(self, fun):
        self.clicked_callback = fun
        self._ui.itemClicked.connect(self._internal_item_clicked_callback)

    def _internal_item_clicked_callback(self, item_clicked, pos):
        clicked_item_content = item_clicked.data(0, Qt.UserRole)

        patient_clicked = item_clicked
        while patient_clicked.parent():
            patient_clicked = patient_clicked.parent()
        patient_clicked_content = patient_clicked.data(0, Qt.UserRole)

        self.clicked_callback(patient_clicked_content, clicked_item_content)

    def set_custom_context_menu(self, fun):
        self.context_menu_callback = fun
        self._ui.setContextMenuPolicy(Qt.CustomContextMenu)
        self._ui.customContextMenuRequested.connect(self._internal_context_menu_callback)

    def _internal_context_menu_callback(self, pos):
        item_clicked = self._ui.selectedItems()
        if item_clicked:
            clicked_item_content = item_clicked[0].data(0, Qt.UserRole)

            patient_clicked = item_clicked[0]
            while patient_clicked.parent():
                patient_clicked = patient_clicked.parent()
            patient_clicked_content = patient_clicked.data(0, Qt.UserRole)
        else:
            clicked_item_content = None
            patient_clicked_content = None

        self.context_menu_callback(patient_clicked_content, clicked_item_content, pos)
