import logging

from PyQt5.QtWidgets import QMenu
import pytrip.tripexecuter as pte

logger = logging.getLogger(__name__)


class TreeWidgetContextMenu:
    def __init__(self, cont):
        self._ui = cont._view._ui
        self._cont = cont

        self._clicked_patient = None
        self._clicked_item = None

        # callbacks
        self.new_patient_callback = None
        self.open_voxelplan_callback = None
        self.add_new_plan_callback = None
        self.execute_plan_callback = None

    def custom_context_menu_callback(self, patient, item, pos):
        self._clicked_patient = patient
        self._clicked_item = item

        popup_menu = QMenu(self._ui)
        if self.new_patient_callback:
            popup_menu.addAction("Add new Patient", self.new_patient_callback)

        if patient:
            if self.open_voxelplan_callback:
                popup_menu.addAction("Open Voxel Plan", self.open_voxelplan_callback)
            popup_menu.addSeparator()
            if self.add_new_plan_callback:
                popup_menu.addAction("Add new plan", self.add_new_plan_callback)

        if isinstance(item, pte.Plan):
            popup_menu.addAction("Edit plan", self._edit_plan)
            popup_menu.addAction("Execute this plan", self._execute_plan_callback)
            popup_menu.addSeparator()
            popup_menu.addAction("Add new field", self._add_new_field)

        if isinstance(item, pte.Field):
            popup_menu.addSeparator()
            popup_menu.addAction("Edit field", self._edit_field)

        node = self._ui.mapToGlobal(pos)
        popup_menu.exec_(node)

        self._cont.synchronize()

    def _execute_plan_callback(self):
        if self.execute_plan_callback:
            self.execute_plan_callback(self._clicked_patient, self._clicked_item)

    def _edit_plan(self):
        self._clicked_patient.edit_plan(self._clicked_item)

    def _add_new_field(self):
        self._clicked_patient.add_new_field(self._clicked_item)

    def _edit_field(self):
        self._clicked_patient.edit_field(self._clicked_item)
