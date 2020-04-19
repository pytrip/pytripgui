import logging

logger = logging.getLogger(__name__)


class TreeController:
    def __init__(self, model, view):
        """
        edit_item_callback is called when user wants to add new, or edit existing item: edit_item(item_to_edit)
        Callback function should return False if user canceled operation, or True if approved
        """
        self.edit_item_callback = None
        self.open_voxelplan_callback = None
        self.execute_plan_callback = None

        # internal
        self._tree_model = model
        self._view = view
        self._view.internal_events.on_add_child += self._add_new_item_callback
        self._view.internal_events.on_edit_selected_item += self._edit_selected_item_callback
        self._view.internal_events.on_open_voxelplan += self._open_voxelplan_callback
        self._view.internal_events.on_execute += self._execute_callback

    def _add_new_item_callback(self):
        child = None
        save_data = True

        if self._view.selected_item:
            child = self._view.selected_item.child_class()
            if self.edit_item_callback:
                save_data = self.edit_item_callback(child, self._view.selected_item)

        if save_data:
            self._tree_model.insertRows(0, 1, self._view.selected_q_item, child)

    def _edit_selected_item_callback(self):
        self.edit_item_callback(self._view.selected_item, self._view.selected_item_patient)

    def _open_voxelplan_callback(self):
        self.open_voxelplan_callback(self._view.selected_item)

    def _execute_callback(self):
        self.execute_plan_callback(self._view.selected_item, self._view.selected_item_patient)
