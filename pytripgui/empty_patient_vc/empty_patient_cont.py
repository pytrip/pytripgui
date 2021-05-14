from pytrip.cube import Cube
from pytrip.ctx import CtxCube
from pytrip.vdx import VdxCube, create_sphere

import logging

logger = logging.getLogger(__name__)


class EmptyPatientController(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.is_cancelled = False
        self._setup_callbacks()

    def _setup_callbacks(self):
        self.view.set_ok_callback(self._save_and_exit)
        self.view.set_cancel_callback(self._cancel)

        self.view.add_organ_button.emit_on_click(
            lambda: self.view.organ_table.add_row())

    def _save_and_exit(self):
        if self._validate_fields():
            self._set_model_from_view()
        self._exit()

    def _cancel(self):
        self.is_cancelled = True
        self._exit()

    def _exit(self):
        self.view.exit()

    def _set_model_from_view(self):
        cube = Cube()

        cube.create_empty_cube(
            value=0,
            dimx=int(self.view.width.text),
            dimy=int(self.view.height.text),
            dimz=int(self.view.depth.text),
            pixel_size=1,
            slice_distance=int(self.view.distanceBetweenSlices.text)
        )
        
        self.model.ctx = CtxCube(cube)
        self.model.ctx.basename = self.view.patientName.text

        vdxCube = VdxCube(self.model.ctx)
        vdxCube.basename = self.view.patientName.text

        for row in range(self.view.organ_table.row_count()):
            voi = create_sphere(
                cube=self.model.ctx,
                name=self.view.organ_table.item(row, 0).text(),
                center=[
                    int(self.view.organ_table.item(row, 1).text()),
                    int(self.view.organ_table.item(row, 2).text()),
                    int(self.view.organ_table.item(row, 3).text()),
                ],
                radius=int(self.view.organ_table.item(row, 4).text()))
            vdxCube.add_voi(voi)

        self.model.vdx = vdxCube
        self.model.name = self.view.patientName.text

    # TODO
    def _validate_fields(self):
        return True
