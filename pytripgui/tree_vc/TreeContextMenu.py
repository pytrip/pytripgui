import logging

from PyQt5.QtWidgets import QMenu

logger = logging.getLogger(__name__)


class TreeContextMenu:
    def __init__(self, parent_view, tree_cont):
        self._parent_view = parent_view
        self._tree_controller = tree_cont

        self._clicked_patient = None
        self._clicked_item = None

    def custom_context_menu_callback(self, patient, item, pos):
        self._clicked_patient = patient
        self._clicked_item = item

        popup_menu = QMenu(self._parent_view)
        popup_menu.addAction("Add new Patient", self._tree_controller.add_new_patient)
        popup_menu.addSeparator()

        node = self._parent_view.mapToGlobal(pos)
        popup_menu.exec_(node)
