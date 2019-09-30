from PyQt5.QtWidgets import QMenu
import pytrip.tripexecuter as pte
from pytripgui.model.patient import Patient

import logging
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

    def custom_context_menu_callback(self, patient, item, pos):
        self._clicked_patient = patient
        self._clicked_item = item

        popup_menu = QMenu(self._ui)
        popup_menu.addAction("Add new Patient", self._add_new_patient)

        if patient:
            popup_menu.addSeparator()
            popup_menu.addAction("Add new plan", self._add_new_plan)
            popup_menu.addAction("Open Voxel Plan", self._open_voxelplan)

        if isinstance(item, pte.Plan):
            popup_menu.addAction("Edit plan", self._edit_plan)
            popup_menu.addAction("Add new field", self._add_new_field)

        if isinstance(item, pte.Field):
            popup_menu.addSeparator()
            popup_menu.addAction("Edit field", self._edit_field)

        node = self._ui.mapToGlobal(pos)
        popup_menu.exec_(node)

        self._cont.synchronize()

    def _add_new_patient(self):
        if self.new_patient_callback:
            self.new_patient_callback()

    def _open_voxelplan(self):
        if self.open_voxelplan_callback:
            self.open_voxelplan_callback()

    def _add_new_plan(self):
        self._clicked_patient.add_new_plan()

    def _edit_plan(self):
        self._clicked_patient.edit_plan(self._clicked_item)

    def _add_new_field(self):
        self._clicked_patient.add_new_field(self._clicked_item)

    def _edit_field(self):
        self._clicked_patient.edit_field(self._clicked_item)
