from PyQt5.QtWidgets import QMenu
import pytrip.tripexecuter as pte

import logging
logger = logging.getLogger(__name__)


class TreeWidgetContextMenu:
    def __init__(self, cont):
        self._ui = cont._view._ui
        self._cont = cont

    def custom_context_menu_callback(self, patient, item, pos):
        self._clicked_patient = patient
        self._clicked_item = item

        popup_menu = QMenu(self._ui)
        popup_menu.addAction("Add new plan", self._add_new_plan)

        if isinstance(item, pte.Plan):
            popup_menu.addAction("Edit plan", self._edit_plan)
            popup_menu.addSeparator()
            popup_menu.addAction("Add new field", self._add_new_field)

        if isinstance(item, pte.Field):
            popup_menu.addSeparator()
            popup_menu.addAction("Edit field", self._edit_field)

        node = self._ui.mapToGlobal(pos)
        popup_menu.exec_(node)

        self._cont.synchronize()

    def _add_new_plan(self):
        self._clicked_patient.add_new_plan()

    def _edit_plan(self):
        self._clicked_patient.edit_plan(self._clicked_item)

    def _add_new_field(self):
        self._clicked_patient.add_new_field(self._clicked_item)

    def _edit_field(self):
        self._clicked_patient.edit_field(self._clicked_item)
