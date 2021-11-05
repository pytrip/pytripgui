from pytripgui.view.qt_view_adapter import ComboBox, Label
from pytripgui.view.qt_gui import AddVOIDialog

import logging

logger = logging.getLogger(__name__)


class AddSingleVOIQtView:
    """
    """
    def __init__(self, parent=None):
        self._ui = AddVOIDialog(parent)
        self.voi_combobox = ComboBox(self._ui.VOI_comboBox)
        self.voi_layout = self._ui.VOI_layout

        self.info = Label(self._ui.info_label)

        self.accept = self._ui.accept
        self.accept_buttons = self._ui.accept_buttonBox

    def show(self) -> None:
        self._ui.show()
        # try to not cover vital info of parent dialog (patient limits)
        self._ui.move(self._ui.pos().x(), 1.3 * self._ui.pos().y())
        self._ui.exec_()

    def exit(self) -> None:
        self._ui.close()
