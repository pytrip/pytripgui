from pytripgui.view.qt_view_adapter import LineEdit, TabWidget, LineEditMath
from pytripgui.view.qt_gui import EmptyPatientDialog

import logging

logger = logging.getLogger(__name__)


class EmptyPatientQtView:
    """
    """
    def __init__(self, parent=None):
        self._ui = EmptyPatientDialog(parent)
        self.name = LineEdit(self._ui.name_lineEdit)
        self.hu_value = LineEditMath(self._ui.hUValue_lineEdit)

        self.dimensions_tabs = TabWidget(self._ui.dimensions_tabWidget)
        self.dimensions_fields = [{
            "width": LineEditMath(self._ui.width_lineEdit_1),
            "height": LineEditMath(self._ui.height_lineEdit_1),
            "depth": LineEditMath(self._ui.depth_lineEdit_1),
            "slice_distance": LineEditMath(self._ui.sliceDistance_lineEdit_1),
            "pixel_size": LineEditMath(self._ui.pixelSize_lineEdit_1),
        }, {
            "width": LineEditMath(self._ui.width_lineEdit_2),
            "height": LineEditMath(self._ui.height_lineEdit_2),
            "depth": LineEditMath(self._ui.depth_lineEdit_2),
            "slice_number": LineEditMath(self._ui.sliceNumber_lineEdit_2),
            "pixel_number_x": LineEditMath(self._ui.pixelNumberX_lineEdit_2),
            "pixel_number_y": LineEditMath(self._ui.pixelNumberY_lineEdit_2),
        }, {
            "slice_number": LineEditMath(self._ui.sliceNumber_lineEdit_3),
            "slice_distance": LineEditMath(self._ui.sliceDistance_lineEdit_3),
            "pixel_number_x": LineEditMath(self._ui.pixelNumberX_lineEdit_3),
            "pixel_number_y": LineEditMath(self._ui.pixelNumberY_lineEdit_3),
            "pixel_size": LineEditMath(self._ui.pixelSize_lineEdit_3),
        }]

        self.xoffset = LineEditMath(self._ui.xOffset_lineEdit)
        self.yoffset = LineEditMath(self._ui.yOffset_lineEdit)
        self.slice_offset = LineEditMath(self._ui.sliceOffset_lineEdit)

        self.accept = self._ui.accept
        self.accept_buttons = self._ui.accept_buttonBox

    def show(self) -> None:
        self._ui.show()
        self._ui.exec_()

    def exit(self) -> None:
        self._ui.close()
