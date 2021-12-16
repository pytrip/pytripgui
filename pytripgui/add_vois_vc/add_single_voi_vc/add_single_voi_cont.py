from pytrip.vdx import create_sphere, create_cube, create_cylinder

import logging

from pytripgui.add_vois_vc.add_single_voi_vc.custom_voi.custom_voi_cont import CustomVOIController
from pytripgui.add_vois_vc.add_single_voi_vc.custom_voi.custom_voi_view import CustomVOIQtView
from pytripgui.add_vois_vc.voi_widget import VOIWidget, SphericalVOIWidget, CuboidalVOIWidget, CylindricalVOIWidget,\
    CustomVOIWidget

logger = logging.getLogger(__name__)


class AddSingleVOIController:
    def __init__(self, model, view, used_voi_names):
        self.model = model
        self.view = view
        self.used_voi_names = used_voi_names
        self.is_accepted = False
        self._setup_callbacks()

        self.voi_types = {"Spherical": SphericalVOIWidget, "Cuboidal": CuboidalVOIWidget,
                          "Cylindrical": CylindricalVOIWidget, "Custom": CustomVOIWidget}
        self._reload_voi()

    def _setup_callbacks(self) -> None:
        self.view.accept_buttons.accepted.disconnect()
        self.view.accept_buttons.accepted.connect(self._save_and_exit)

        self.view.voi_combobox.emit_on_item_change(self._reload_voi)

    def _save_and_exit(self) -> None:
        if self._validate_voi():
            # if it's a custom voi, open another dialog for the next step in its creation
            voi_type = self.view.voi_combobox.current_text
            if voi_type == "Custom":
                if not self._create_custom_voi_dialog():
                    return
            self.is_accepted = True
            self.view.accept()

    def _create_custom_voi_dialog(self) -> bool:
        view = CustomVOIQtView(self.view.get_ui())

        voi_widget = self.view.voi_layout.itemAt(0).widget()
        limits = [voi_widget.width_height, voi_widget.width_height, voi_widget.depth]
        center = voi_widget.center
        controller = CustomVOIController(self.model, view, limits, center)

        view.show()

        if controller.is_accepted:
            slices = controller.get_slices()
            self.view.voi_layout.itemAt(0).widget().slices = slices
            return True
        return False

    def _reload_voi(self) -> None:
        voi_type = self.view.voi_combobox.current_text
        if voi_type in self.voi_types:
            # if there is already some layout loaded then close it
            if self.view.voi_layout.count():
                self.view.voi_layout.itemAt(0).widget().close()
            voi = self.voi_types[voi_type]
            self.view.voi_layout.insertWidget(0, voi())

    def _validate_voi(self) -> bool:
        voi_widget = self.view.voi_layout.itemAt(0).widget()
        # validate fields
        if not voi_widget.validate():
            return False

        # check if name isn't already being used
        if voi_widget.name.lower() in self.used_voi_names:
            self.view.info.text = "This name is already being used by another VOI."
            return False

        ctx = self.model
        center_no_offsets = [a - b for (a, b) in zip(voi_widget.center, [ctx.xoffset, ctx.yoffset, ctx.zoffset])]
        if isinstance(voi_widget, CustomVOIWidget):
            # TODO just for easy checking of limits, for now
            voi = create_cube(
                cube=ctx,
                name=voi_widget.name,
                center=center_no_offsets,
                width=voi_widget.width_height,
                height=voi_widget.width_height,
                depth=voi_widget.depth
            )
        elif isinstance(voi_widget, SphericalVOIWidget):
            voi = create_sphere(
                cube=ctx,
                name=voi_widget.name,
                center=center_no_offsets,
                radius=voi_widget.radius
            )
        elif isinstance(voi_widget, CuboidalVOIWidget):
            voi = create_cube(
                cube=ctx,
                name=voi_widget.name,
                center=center_no_offsets,
                width=voi_widget.width,
                height=voi_widget.height,
                depth=voi_widget.depth
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
            return False

        # validate containment in ctx
        if not voi.is_fully_contained():
            self.view.info.text = "VOI isn't fully contained in the given patient."
            return False
        return True

    def get_voi_widget(self) -> VOIWidget:
        return self.view.voi_layout.itemAt(0).widget()
