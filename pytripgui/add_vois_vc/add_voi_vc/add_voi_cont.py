from pytrip.vdx import create_sphere, create_cube

import logging

from pytripgui.add_vois_vc.voi_widget import SphericalVOIWidget, CuboidalVOIWidget

logger = logging.getLogger(__name__)


class AddVOIController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.is_accepted = False
        self._setup_callbacks()

        self.voi_types = {
            "Spherical": SphericalVOIWidget,
            "Cuboidal": CuboidalVOIWidget
        }
        self._reload_voi()

    def _setup_callbacks(self):
        self.view.accept_buttons.accepted.disconnect()
        self.view.accept_buttons.accepted.connect(self._save_and_exit)

        self.view.voi_combobox.emit_on_item_change(self._reload_voi)

    def _save_and_exit(self):
        if self._validate_voi():
            self.is_accepted = True
            self.view.accept()

    def _reload_voi(self):
        voi_type = self.view.voi_combobox.current_text
        if voi_type in self.voi_types:
            if self.view.voi_layout.count():
                self.view.voi_layout.itemAt(0).widget().close()
            voi = self.voi_types[voi_type]
            self.view.voi_layout.insertWidget(0, voi())

    def _validate_voi(self):
        voi_widget = self.view.voi_layout.itemAt(0).widget()
        # validate fields
        if not voi_widget.validate():
            return False

        ctx = self.model
        if isinstance(voi_widget, SphericalVOIWidget):
            voi = create_sphere(
                cube=ctx,
                name=voi_widget.name,
                center=voi_widget.center,
                radius=voi_widget.radius
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
            return False

        # validate containment in ctx
        # TODO show information somewhere about improper containment
        if voi.is_fully_contained():
            voi_widget.highlight_border(False)
            return True
        else:
            voi_widget.highlight_border(True)
            return False

    def get_voi_widget(self):
        return self.view.voi_layout.itemAt(0).widget()