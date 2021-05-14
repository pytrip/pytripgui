from pytripgui.view.qt_view_adapter import LineEdit, TableWidget, ComboBox, UserInfoBox, PushButton
from pytripgui.view.qt_gui import EmptyPatientDialog

import logging

logger = logging.getLogger(__name__)


class EmptyPatientQtView(object):
    """
    """
    def __init__(self, parent=None):
        self._ui = EmptyPatientDialog(parent)

        self.width = LineEdit(self._ui.width_lineEdit)
        self.height = LineEdit(self._ui.height_lineEdit)
        self.depth = LineEdit(self._ui.depth_lineEdit)
        self.distanceBetweenSlices = LineEdit(
            self._ui.distanceBetweenSlices_lineEdit)
        self.patientName = LineEdit(self._ui.patientName_lineEdit)

        self.organ_table = TableWidget(self._ui.organ_tableWidget)

        self.add_organ_button = PushButton(self._ui.addOrgan_pushButton)

    def show(self):
        self._ui.show()
        self._ui.exec_()

    def exit(self):
        self._ui.close()

    def set_ok_callback(self, fun):
        self._ui.accept_buttonBox.accepted.connect(fun)

    def set_cancel_callback(self, fun):
        self._ui.accept_buttonBox.rejected.connect(fun)
