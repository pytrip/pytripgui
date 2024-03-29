import logging
from typing import Optional

from numpy import unravel_index

from pytripgui.canvas_vc.objects.ctx import Ctx
from pytripgui.canvas_vc.objects.dos import Dos
from pytripgui.canvas_vc.objects.let import Let
from pytripgui.canvas_vc.objects.vdx import Vdx
from pytripgui.canvas_vc.projection_selector import ProjectionSelector

logger = logging.getLogger(__name__)


class PlotModel:
    def __init__(self, projection_selector=ProjectionSelector()):

        self.vdx: Optional[Vdx] = None  # cube is also in the main_model, but here this is specific for plotting.

        self.projection_selector = projection_selector
        self.display_filter = ""
        self.dose: Optional[Dos] = None
        self.let: Optional[Let] = None
        self.ctx: Optional[Ctx] = None

        # These are used by getters and setters, must come after the other values are initialized.
        self.cube = None
        self.slice_pos_mm: float = 0.0

    def set_ctx(self, ctx):
        self.ctx = Ctx(ctx, self.projection_selector)
        if not self.projection_selector.is_loaded():
            self.projection_selector.load_slices_count(ctx)

    def set_let(self, let):
        self.let = Let(let, self.projection_selector)
        if not self.projection_selector.is_loaded():
            self.projection_selector.load_slices_count(let)

    def set_dose(self, dose):
        self.dose = Dos(dose, self.projection_selector)
        if not self.projection_selector.is_loaded():
            self.projection_selector.load_slices_count(dose)

            max_item_index = unravel_index(dose.cube.argmax(), dose.cube.shape)
            self.projection_selector._transversal_slice_no = max_item_index[0]
            self.projection_selector._sagittal_slice_no = max_item_index[2]
            self.projection_selector._coronal_slice_no = max_item_index[1]

    def set_vdx(self):
        self.vdx = Vdx(self.ctx.cube, self.projection_selector)
