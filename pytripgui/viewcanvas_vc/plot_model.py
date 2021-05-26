import logging

from numpy import unravel_index

from pytripgui.viewcanvas_vc.objects.dos import Dos
from pytripgui.viewcanvas_vc.objects.let import Let
from pytripgui.viewcanvas_vc.objects.ctx import Ctx
from pytripgui.viewcanvas_vc.objects.vdx import Vdx

logger = logging.getLogger(__name__)


class ProjectionSelector:
    def __init__(self):
        self._transversal_slice_no = 0
        self._sagittal_slice_no = 0
        self._coronal_slice_no = 0

        self._transversal_last_slice_no = 0
        self._sagittal_last_slice_no = 0
        self._coronal_last_slice_no = 0

        # "Transversal" (xy)
        # "Sagittal" (yz)
        # "Coronal"  (xz)
        self.plane = "Transversal"

    def next_slice(self):
        self.current_slice_no = (self.current_slice_no + 1) % self.last_slice_no

    def prev_slice(self):
        self.current_slice_no = (self.current_slice_no - 1) % self.last_slice_no

    def get_projection(self, data):
        if self.plane == "Transversal":
            return data.cube[self.current_slice_no]
        if self.plane == "Sagittal":
            return data.cube[-1:0:-1, -1:0:-1, self.current_slice_no]
        if self.plane == "Coronal":
            return data.cube[-1:0:-1, self.current_slice_no, -1:0:-1]

    def load_slices_count(self, data):
        self._transversal_last_slice_no = data.dimz
        self._sagittal_last_slice_no = data.dimy
        self._coronal_last_slice_no = data.dimx

        self._transversal_slice_no = self._transversal_last_slice_no // 2
        self._sagittal_slice_no = self._sagittal_last_slice_no // 2
        self._coronal_slice_no = self._coronal_last_slice_no // 2

    @property
    def current_slice_no(self):
        if self.plane == "Transversal":
            return self._transversal_slice_no
        if self.plane == "Sagittal":
            return self._sagittal_slice_no
        if self.plane == "Coronal":
            return self._coronal_slice_no

    @current_slice_no.getter
    def current_slice_no(self):
        if self.plane == "Transversal":
            return self._transversal_slice_no
        if self.plane == "Sagittal":
            return self._sagittal_slice_no
        if self.plane == "Coronal":
            return self._coronal_slice_no

    @current_slice_no.setter
    def current_slice_no(self, position):
        if self.plane == "Transversal":
            self._transversal_slice_no = position
        if self.plane == "Sagittal":
            self._sagittal_slice_no = position
        if self.plane == "Coronal":
            self._coronal_slice_no = position

    @property
    def last_slice_no(self):
        if self.plane == "Transversal":
            return self._transversal_last_slice_no
        if self.plane == "Sagittal":
            return self._sagittal_last_slice_no
        if self.plane == "Coronal":
            return self._coronal_last_slice_no


class PlotModel(object):
    def __init__(self):

        self.vdx = None  # cube is also in the main_model, but here this is specific for plotting.
        self.vois = [
        ]  # list of actual vois to be plotted (this may be fewer than vois in the self.vdx)

        self.projection_selector = ProjectionSelector()
        self.display_filter = ""
        self.dose = None
        self.let = None
        self.ctx = None

        # These are used by getters and setters, must come after the other values are initialized.
        self.cube = None
        self.slice_pos_mm = 0.0

    def set_ctx(self, ctx):
        self.ctx = Ctx(self.projection_selector)
        self.ctx.cube = ctx
        self.projection_selector.load_slices_count(ctx)

    def set_let(self, let):
        self.let = Let(self.projection_selector)
        self.let.cube = let
        self.projection_selector.load_slices_count(let)

    def set_dose(self, dose):
        self.dose = Dos(self.projection_selector)
        self.dose.cube = dose
        self.projection_selector.load_slices_count(dose)

        max_item_index = unravel_index(dose.cube.argmax(), dose.cube.shape)
        self.projection_selector._transversal_slice_no = max_item_index[0]
        self.projection_selector._sagittal_slice_no = max_item_index[2]
        self.projection_selector._coronal_slice_no = max_item_index[1]

    def set_vdx(self):
        self.vdx = Vdx(self.projection_selector)
        self.vdx.vois = []
        self.vdx.ctx = self.ctx.cube
