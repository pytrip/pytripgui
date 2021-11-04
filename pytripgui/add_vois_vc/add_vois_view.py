from pytripgui.view.qt_view_adapter import PushButton, Label
from pytripgui.view.qt_gui import AddVOIsDialog

import logging

logger = logging.getLogger(__name__)


class AddVOIsQtView:
    """
    """
    def __init__(self, parent=None):
        self._ui = AddVOIsDialog(parent)
        self.name = Label(self._ui.name_label)
        self.width = Label(self._ui.width_label)
        self.height = Label(self._ui.height_label)
        self.depth = Label(self._ui.depth_label)
        self.pixel_size = Label(self._ui.pixelSize_label)
        self.pixel_number_x = Label(self._ui.pixelNumberX_label)
        self.pixel_number_y = Label(self._ui.pixelNumberY_label)
        self.slice_number = Label(self._ui.sliceNumber_label)
        self.slice_distance = Label(self._ui.sliceDistance_label)
        self.x_offset = Label(self._ui.xOffset_label)
        self.y_offset = Label(self._ui.yOffset_label)
        self.slice_offset = Label(self._ui.sliceOffset_label)

        self.x_min = Label(self._ui.xMin_label)
        self.x_max = Label(self._ui.xMax_label)
        self.y_min = Label(self._ui.yMin_label)
        self.y_max = Label(self._ui.yMax_label)
        self.z_min = Label(self._ui.zMin_label)
        self.z_max = Label(self._ui.zMax_label)

        self.voi_scroll_area = self._ui.voi_scrollArea

        self.add_voi_button = PushButton(self._ui.addVOI_pushButton)

        self.accept = self._ui.accept
        self.accept_buttons = self._ui.accept_buttonBox

    def show(self) -> None:
        self._ui.show()
        self._ui.exec_()

    def exit(self) -> None:
        self._ui.close()
