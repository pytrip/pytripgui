from PyQt5.QtWidgets import QMenu

import logging
logger = logging.getLogger(__name__)


class TreeWidgetContextMenu:
    def __init__(self, cont):
        self._ui = cont._view._ui
        self._cont = cont
        self._current_patient = None
        self._current_item = None

    def custom_context_menu_callback(self, patient, item, pos):
        self._current_patient = patient
        self._current_item = item

        popup_menu = QMenu(self._ui)
        popup_menu.addAction("Add new plan", self._add_new_plan)
        popup_menu.addSeparator()
        popup_menu.addAction("Open DICOM", self.non)
        popup_menu.addSeparator()
        popup_menu.addAction("Open DICOM", self.non)
        popup_menu.addSeparator()
        popup_menu.addAction("Open DICOM", self.non)
        popup_menu.addSeparator()
        popup_menu.addAction("Open DICOM", self.non)
        node = self._ui.mapToGlobal(pos)
        popup_menu.exec_(node)

        self._cont.synchronize()

    def _add_new_plan(self):
        self._current_patient.add_new_plan()

    def non(self):
        pass
