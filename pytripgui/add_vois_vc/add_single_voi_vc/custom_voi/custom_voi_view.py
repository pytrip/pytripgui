from pytripgui.view.qt_view_adapter import Label, PushButton, LineEdit, LineEditMath
from pytripgui.view.qt_gui import CustomVOIDialog

import logging

logger = logging.getLogger(__name__)


class CustomVOIQtView:
    """
    """
    def __init__(self, parent=None):
        self._ui = CustomVOIDialog(parent)
        self.draw_layout = self._ui.draw_horizontalLayout
        self.new_contour_button = PushButton(self._ui.newContour_pushButton)

        # TODO disable some of these if current slice is already at the top/bottom
        self.up_slice_button = PushButton(self._ui.upSlice_pushButton)
        self.top_slice_button = PushButton(self._ui.topSlice_pushButton)
        self.down_slice_button = PushButton(self._ui.downSlice_pushButton)
        self.bottom_slice_button = PushButton(self._ui.bottomSlice_pushButton)
        self.clear_slice_button = PushButton(self._ui.clearSlice_pushButton)
        self.clear_all_button = PushButton(self._ui.clearAll_pushButton)
        self.slice_index = LineEdit(self._ui.sliceIndex_lineEdit)
        self.info = Label(self._ui.info_label)

        self.add_point_button = PushButton(self._ui.addPoint_pushButton)
        # TODO add validation
        self.point_x = LineEditMath(self._ui.pointX_lineEdit)
        self.point_y = LineEditMath(self._ui.pointY_lineEdit)

        self.extend_up_button = PushButton(self._ui.extendUp_pushButton)
        self.extend_down_button = PushButton(self._ui.extendDown_pushButton)
        self.extend_slice = LineEdit(self._ui.extendSlice_lineEdit)

        self.slice_min = Label(self._ui.sliceMin_label)
        self.slice_max = Label(self._ui.sliceMax_label)

        self.undo_button = PushButton(self._ui.undo_pushButton)
        self.redo_button = PushButton(self._ui.redo_pushButton)

        self.accept = self._ui.accept
        self.accept_buttons = self._ui.accept_buttonBox

    def show(self) -> None:
        self._ui.show()
        self._ui.exec_()

    def exit(self) -> None:
        self._ui.close()
