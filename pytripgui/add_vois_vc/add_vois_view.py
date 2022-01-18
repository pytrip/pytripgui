from pytripgui.view.qt_view_adapter import PushButton, Label
from pytripgui.view.qt_gui import AddVOIsDialog

import logging

logger = logging.getLogger(__name__)


class AddVOIsQtView:
    """
    """
    def __init__(self, parent=None):
        self.ui = AddVOIsDialog(parent)
        self.name = Label(self.ui.name_label)
        self.width = Label(self.ui.width_label)
        self.height = Label(self.ui.height_label)
        self.depth = Label(self.ui.depth_label)
        self.pixel_size = Label(self.ui.pixelSize_label)
        self.pixel_number_x = Label(self.ui.pixelNumberX_label)
        self.pixel_number_y = Label(self.ui.pixelNumberY_label)
        self.slice_number = Label(self.ui.sliceNumber_label)
        self.slice_distance = Label(self.ui.sliceDistance_label)
        self.x_offset = Label(self.ui.xOffset_label)
        self.y_offset = Label(self.ui.yOffset_label)
        self.slice_offset = Label(self.ui.sliceOffset_label)

        self.x_min = Label(self.ui.xMin_label)
        self.x_max = Label(self.ui.xMax_label)
        self.y_min = Label(self.ui.yMin_label)
        self.y_max = Label(self.ui.yMax_label)
        self.z_min = Label(self.ui.zMin_label)
        self.z_max = Label(self.ui.zMax_label)

        self.voi_scroll_area = self.ui.voi_scrollArea

        self.add_voi_button = PushButton(self.ui.addVOI_pushButton)

        self.accept = self.ui.accept
        self.accept_buttons = self.ui.accept_buttonBox

    def show(self) -> None:
        self.ui.show()
        self.ui.exec_()

    def exit(self) -> None:
        self.ui.close()
