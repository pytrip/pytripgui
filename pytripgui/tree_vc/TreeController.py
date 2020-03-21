import logging

from pytripgui.tree_vc.TreeContextMenu import TreeContextMenu

from pytripgui.tree_vc.TreeItems import PatientItem

logger = logging.getLogger(__name__)


class TreeController:
    def __init__(self, model, view):
        self._tree_model = model
        self._view = view
        self.context_menu = TreeContextMenu(view, self)

        self._view.set_item_clicked_callback(self._clicked_item_callback)
        self.update_selected_item_callback = None

        self._view.set_custom_context_menu(self.context_menu.custom_context_menu_callback)

    def _clicked_item_callback(self, clicked_patient, clicked_item):
        self._view.set_header_label("Patient: " + clicked_patient.name)
        if self.update_selected_item_callback:
            self.update_selected_item_callback(clicked_patient, clicked_item)

    def add_new_patient(self):
        print("############################################################")
        self._tree_model._root_item.add_child(PatientItem())
        self._tree_model.invalidate()
