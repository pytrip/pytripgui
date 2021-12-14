from PyQt5 import QtWidgets, uic
from pathlib import Path
import logging

from pytripgui.add_vois_vc.add_single_voi_vc.add_single_voi_cont import AddSingleVOIController
from pytripgui.add_vois_vc.add_single_voi_vc.add_single_voi_view import AddSingleVOIQtView
from pytripgui.add_vois_vc.voi_widget import SphericalVOIWidget, CuboidalVOIWidget, CylindricalVOIWidget
from pytripgui.view.qt_view_adapter import PushButton
from pytrip.vdx import create_sphere, create_cube, create_cylinder

logger = logging.getLogger(__name__)


class AddVOIsController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.is_accepted = False
        self._setup_callbacks()

        self._set_view_from_model()

        # used for rejecting repeated voi names
        self.existing_vois_names = [voi.name.lower() for voi in self.model.vdx.vois]

    def _setup_callbacks(self) -> None:
        self.view.accept_buttons.accepted.disconnect()
        self.view.accept_buttons.accepted.connect(self._save_and_exit)

        self.view.add_voi_button.emit_on_click(lambda: self._create_add_voi_dialog())

    def _save_and_exit(self) -> None:
        self._set_model_from_view()
        self.is_accepted = True
        self.view.accept()

    def _create_add_voi_dialog(self) -> None:
        view = AddSingleVOIQtView()

        # get VOI names that are already being used by the about to be added VOIs
        list_vois = self.view.voi_scroll_area.widget().layout()
        list_vois_names = []
        for index in range(list_vois.count() - 1):
            list_voi_element = list_vois.itemAt(index).widget()
            voi_widget = list_voi_element.voi_space.itemAt(0).widget()
            list_vois_names.append(voi_widget.name.lower())
        controller = AddSingleVOIController(self.model.ctx, view, self.existing_vois_names + list_vois_names)

        view.show()

        if controller.is_accepted:
            voi_widget = controller.get_voi_widget()
            voi_widget.disable_fields()
            list_element_voi = ListElementVOI(voi_widget)
            self.view.voi_scroll_area.widget().layout().insertWidget(0, list_element_voi)

    def _set_view_from_model(self) -> None:
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
        view.x_offset.text = ctx.xoffset
        view.y_offset.text = ctx.yoffset
        view.slice_offset.text = ctx.zoffset

        view.x_min.text = ctx.xoffset
        view.x_max.text = ctx.xoffset + ctx.dimx * ctx.pixel_size
        view.y_min.text = ctx.yoffset
        view.y_max.text = ctx.yoffset + ctx.dimy * ctx.pixel_size
        view.z_min.text = ctx.zoffset
        view.z_max.text = ctx.zoffset + ctx.slice_number * ctx.slice_distance

    def _set_model_from_view(self) -> None:
        ctx = self.model.ctx
        vdx = self.model.vdx

        list_vois = self.view.voi_scroll_area.widget().layout()
        # iterating over every element of the list of vois while ignoring a trailing vertical spacer
        for index in range(list_vois.count() - 1):
            # the actual voi widget is embedded in the list element, we need to shell it
            list_voi_element = list_vois.itemAt(index).widget()
            voi_widget = list_voi_element.voi_space.itemAt(0).widget()
            center_no_offsets = [a - b for (a, b) in zip(voi_widget.center, [ctx.xoffset, ctx.yoffset, ctx.zoffset])]

            if isinstance(voi_widget, SphericalVOIWidget):
                voi = create_sphere(
                    cube=ctx,
                    name=voi_widget.name,
                    center=center_no_offsets,
                    radius=voi_widget.radius,
                )
            elif isinstance(voi_widget, CuboidalVOIWidget):
                voi = create_cube(
                    cube=ctx,
                    name=voi_widget.name,
                    center=center_no_offsets,
                    width=voi_widget.width,
                    height=voi_widget.height,
                    depth=voi_widget.depth,
                )
            elif isinstance(voi_widget, CylindricalVOIWidget):
                voi = create_cylinder(
                    cube=ctx,
                    name=voi_widget.name,
                    center=center_no_offsets,
                    radius=voi_widget.radius,
                    depth=voi_widget.depth,
                )
            else:
                logger.debug("VOI widget unrecognised")
                return
            vdx.add_voi(voi)


class ListElementVOI(QtWidgets.QFrame):
    def __init__(self, voi_widget):
        super().__init__()
        widget_path = Path(Path(__file__).parent, "widgets", "list_element_voi.ui").resolve()
        uic.loadUi(widget_path, self)

        self._remove_button = PushButton(self.remove_pushButton)
        self._remove_button.emit_on_click(self._remove_self)

        self.voi_space.insertWidget(0, voi_widget)

    def _remove_self(self) -> None:
        self.parent().layout().removeWidget(self)
        self.close()
