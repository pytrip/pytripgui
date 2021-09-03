from pytripgui.view.qt_view_adapter import ComboBox
from pytripgui.view.qt_gui import AddVOIDialog

import logging

logger = logging.getLogger(__name__)


class AddVOIQtView:
    """
    """
    def __init__(self, parent=None):
        self._ui = AddVOIDialog(parent)
        self.voi_combobox = ComboBox(self._ui.VOI_comboBox)
        self.voi_layout = self._ui.VOI_layout

        self.accept = self._ui.accept
        self.accept_buttons = self._ui.accept_buttonBox

    def show(self):
        self._ui.show()
        self._ui.exec_()

    def exit(self):
        self._ui.close()
