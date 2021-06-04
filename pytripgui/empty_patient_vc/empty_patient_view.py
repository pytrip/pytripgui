from pytripgui.view.qt_view_adapter import LineEdit, TabWidget, PushButton
from pytripgui.view.qt_gui import EmptyPatientDialog

import logging

logger = logging.getLogger(__name__)


class EmptyPatientQtView(object):
    """
    """
    def __init__(self, parent=None):
        self._ui = EmptyPatientDialog(parent)
        self.name = LineEdit(self._ui.name_lineEdit)
        self.hu_value = LineEdit(self._ui.hUValue_lineEdit)
        self.slice_offset = LineEdit(self._ui.sliceOffset_lineEdit)

        self.dimensions_tabs = TabWidget(self._ui.dimensions_tabWidget)
        self.dimensions_fields = [
            {
                "width": LineEdit(self._ui.width_lineEdit_1),
                "height": LineEdit(self._ui.height_lineEdit_1),
                "depth": LineEdit(self._ui.depth_lineEdit_1),
                "slice_distance": LineEdit(self._ui.sliceDistance_lineEdit_1),
                "pixel_size": LineEdit(self._ui.pixelSize_lineEdit_1),
            },
            {
                "width": LineEdit(self._ui.width_lineEdit_2),
                "height": LineEdit(self._ui.height_lineEdit_2),
                "depth": LineEdit(self._ui.depth_lineEdit_2),
                "slice_number": LineEdit(self._ui.sliceNumber_lineEdit_2),
                "pixel_number_x": LineEdit(self._ui.pixelNumberX_lineEdit_2),
                "pixel_number_y": LineEdit(self._ui.pixelNumberY_lineEdit_2),
            },
            {
                "slice_number": LineEdit(self._ui.sliceNumber_lineEdit_3),
                "slice_distance": LineEdit(self._ui.sliceDistance_lineEdit_3),
                "pixel_number_x": LineEdit(self._ui.pixelNumberX_lineEdit_3),
                "pixel_number_y": LineEdit(self._ui.pixelNumberY_lineEdit_3),
                "pixel_size": LineEdit(self._ui.pixelSize_lineEdit_3),
            }
        ]

        self.voi_scroll_area = self._ui.voi_scrollArea

        self.add_spherical_voi_button = PushButton(self._ui.addSphericalVOI_pushButton)
        self.add_cuboidal_voi_button = PushButton(self._ui.addCuboidalVOI_pushButton)

        self.accept = self._ui.accept
        self.accept_buttons = self._ui.accept_buttonBox

    def show(self):
        self._ui.show()
        self._ui.exec_()

    def exit(self):
        self._ui.close()
