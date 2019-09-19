from pytripgui.model.dos import Dos
from pytripgui.model.let import Let
from pytripgui.model.ctx import Ctx

import pytrip as pt

import logging
logger = logging.getLogger(__name__)


class ProjectionSelector:
    def __init__(self):
        self.current_T_slice = 0
        self.current_S_slice = 0
        self.current_C_slice = 0

        self.max_T_depth = 0
        self.max_S_depth = 0
        self.max_C_depth = 0

        # "Transversal" (xy)
        # "Sagittal" (yz)
        # "Coronal"  (xz)
        self.plane = "Transversal"

    def next_slice(self):
        if self.position < self._max_position():
            self.position += 1
        else:
            self.position = 0

    def prev_slice(self):
        if self.position != 0:
            self.position -= 1
        else:
            self.position = self._max_position()

    def get_projection(self, data):
        if self.plane == "Transversal":
            return data.cube[self.position]
        elif self.plane == "Sagittal":
            return data.cube[-1:0:-1, -1:0:-1, self.position]
        elif self.plane == "Coronal":
            return data.cube[-1:0:-1, self.position, -1:0:-1]

    def load_slices_count(self, data):
        self.max_T_depth = data.dimz - 1
        self.max_S_depth = data.dimy - 1
        self.max_C_depth = data.dimx - 1

        self.current_T_slice = int(self.max_T_depth / 2)
        self.current_S_slice = int(self.max_S_depth / 2)
        self.current_C_slice = int(self.max_C_depth / 2)

    @property
    def position(self):
        if self.plane == "Transversal":
            return self.current_T_slice
        if self.plane == "Sagittal":
            return self.current_S_slice
        if self.plane == "Coronal":
            return self.current_C_slice

    @position.getter
    def position(self):
        if self.plane == "Transversal":
            return self.current_T_slice
        if self.plane == "Sagittal":
            return self.current_S_slice
        if self.plane == "Coronal":
            return self.current_C_slice

    @position.setter
    def position(self, position):
        if self.plane == "Transversal":
            self.current_T_slice = position
        if self.plane == "Sagittal":
            self.current_S_slice = position
        if self.plane == "Coronal":
            self.current_C_slice = position

    def _max_position(self):
        if self.plane == "Transversal":
            return self.max_T_depth
        if self.plane == "Sagittal":
            return self.max_S_depth
        if self.plane == "Coronal":
            return self.max_C_depth


class PlotModel(object):
    def __init__(self):

        # DVHPlot specific
        # TODO: these will be future pt.VolHist objects.
        # Here we shall only keep a list of those dvh's we want to plot.
        self.dvhs = []  # dose volume histograms, list of [x,y] ready for plotting

        # Idea is to attach the VolHist classes to the DosCube objects themselves.
        # The reason for this is, that each DVH will be unique for each DOS. There is only one Vdx loaded.
        # Here in the plotmodel, we will then keep a list of links to those cubes which the user wants to have plotted.

        # LVHPlot specific
        # TODO: these will be future pt.VolHist objects.
        # Here we shall only keep a list of those dvh's we want to plot.
        self.lvhs = []  # let volume histograms, list of [x,y] ready for plotting

        # VDX specific
        self.vdx = None  # cube is also in the main_model, but here this is specific for plotting.
        self.vois = []  # list of actual vois to be plotted (this may be fewer than vois in the self.vdx)
        self.plot_vois = True  # whether all vois are plotted at all

        self.projection_selector = ProjectionSelector()
        self.display_filter = ""
        self.dose = None
        self.let = None
        self.ctx = None

        # Plan specific
        self.plan = None  # Placeholder for plan to be plotted

        # These are used by getters and setters, must come after the other values are initialized.
        self.cube = None
        self.slice_pos_mm = 0.0

    def set_ctx(self, ctx):
        self.ctx = Ctx(self.projection_selector)
        self.ctx.cube = ctx
        self.projection_selector.load_slices_count(ctx)

    def import_let_from_file(self, path):
        logger.debug("Open LetCube {:s}".format(path))
        cube = pt.LETCube()
        cube.read(path)
        self.set_let(cube)

    def set_let(self, let):
        self.let = Let(self.projection_selector)
        self.let.cube = let
        self.projection_selector.load_slices_count(let)

    def import_dose_from_file(self, path):
        logger.debug("Open DosCube {:s}".format(path))
        cube = pt.DosCube()
        cube.read(path)
        self.set_dose(cube)

    def set_dose(self, dose):
        self.dose = Dos(self.projection_selector)
        self.dose.cube = dose
        self.projection_selector.load_slices_count(dose)
