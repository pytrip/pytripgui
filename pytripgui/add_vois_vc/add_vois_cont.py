import os

from PyQt5 import QtWidgets, uic
from pytrip.vdx import create_sphere, create_cube

import logging

from pytripgui.add_vois_vc.add_single_voi_vc.add_single_voi_cont import AddSingleVOIController
from pytripgui.add_vois_vc.add_single_voi_vc.add_single_voi_view import AddSingleVOIQtView
from pytripgui.add_vois_vc.voi_widget import SphericalVOIWidget, CuboidalVOIWidget
from pytripgui.view.qt_view_adapter import PushButton

logger = logging.getLogger(__name__)


class AddVOIsController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.is_accepted = False
        self._setup_callbacks()

        self._set_view_from_model()

    def _setup_callbacks(self):
        self.view.accept_buttons.accepted.disconnect()
        self.view.accept_buttons.accepted.connect(self._save_and_exit)

        self.view.add_voi_button.emit_on_click(lambda: self._create_add_voi_dialog())

    def _save_and_exit(self):
        self._set_model_from_view()
        self.is_accepted = True
        self.view.accept()

    def _create_add_voi_dialog(self):
        view = AddSingleVOIQtView()
        controller = AddSingleVOIController(self.model.ctx, view)

        view.show()

        if not controller.is_accepted:
            return

        voi_widget = controller.get_voi_widget()
        voi_widget.disable_fields()
        list_element_voi = ListElementVOI(voi_widget)
        self.view.voi_scroll_area.widget().layout().insertWidget(0, list_element_voi)

    def _set_view_from_model(self):
        ctx = self.model.ctx
        view = self.view

        view.name.text = ctx.patient_name
        view.width.text = ctx.dimx * ctx.pixel_size
        view.height.text = ctx.dimy * ctx.pixel_size
        view.depth.text = ctx.slice_number * ctx.slice_distance
        view.pixel_size.text = ctx.pixel_size
        view.pixel_number_x.text = ctx.dimx
        view.pixel_number_y.text = ctx.dimy
        view.slice_number.text = ctx.slice_number
        view.slice_distance.text = ctx.slice_distance
        # TODO offsets
        view.slice_offset.text = ctx.zoffset

    def _set_model_from_view(self):
        ctx = self.model.ctx
        vdx = self.model.vdx

        voi_widgets = self.view.voi_scroll_area.widget().layout()
        for index in range(voi_widgets.count() - 1):
            voi_widget = voi_widgets.itemAt(index).widget()

            if isinstance(voi_widget, SphericalVOIWidget):
                voi = create_sphere(
                    cube=ctx,
                    name=voi_widget.name,
                    center=voi_widget.center,
                    radius=voi_widget.radius,
                )
            elif isinstance(voi_widget, CuboidalVOIWidget):
                voi = create_cube(
                    cube=ctx,
                    name=voi_widget.name,
                    center=voi_widget.center,
                    width=voi_widget.width,
                    height=voi_widget.height,
                    depth=voi_widget.depth,
                )
            else:
                logger.debug("VOI widget unrecognised")
                return
            vdx.add_voi(voi)


class ListElementVOI(QtWidgets.QFrame):
    def __init__(self, voi_widget):
        super().__init__()
        path = os.path.join(os.path.curdir, "view", "list_element_voi.ui")
        uic.loadUi(path, self)

        self._remove_button = PushButton(self.remove_pushButton)
        self._remove_button.emit_on_click(self._remove_self)

        self.voi_space.insertWidget(0, voi_widget)

    def _remove_self(self):
        self.parent().layout().removeWidget(self)
        self.close()
