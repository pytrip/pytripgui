from pytripgui.model.dos import Dos
from pytripgui.model.let import Let
from pytripgui.model.ctx import Ctx

import pytrip as pt

import logging
logger = logging.getLogger(__name__)


class ProjectionSelector:
    def __init__(self):
        self.current_x_slice = 50
        self.current_y_slice = 125
        self.current_z_slice = 125

        # "Transversal" (xy)
        # "Sagittal" (yz)
        # "Coronal"  (xz)
        self.plane = "Transversal"

    def next_slice(self):
        if self.plane == "Transversal":
            self.current_x_slice += 1
        if self.plane == "Sagittal":
            self.current_y_slice += 1
        if self.plane == "Coronal":
            self.current_z_slice += 1

    def prev_slice(self):
        if self.plane == "Transversal":
            self.current_x_slice -= 1
        if self.plane == "Sagittal":
            self.current_y_slice -= 1
        if self.plane == "Coronal":
            self.current_z_slice -= 1

    def get_projection(self, data):
        if self.plane == "Transversal":
            return data.cube[self.current_x_slice]
        elif self.plane == "Sagittal":
            return data.cube[-1:0:-1, -1:0:-1, self.current_y_slice]
        elif self.plane == "Coronal":
            return data.cube[-1:0:-1, self.current_z_slice, -1:0:-1]


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

    def import_let_from_file(self, path):
        logger.debug("Open LetCube {:s}".format(path))
        cube = pt.LETCube()
        cube.read(path)
        self.set_let(cube)

    def set_let(self, let):
        self.let = Let(self.projection_selector)
        self.let.cube = let

    def import_dose_from_file(self, path):
        logger.debug("Open DosCube {:s}".format(path))
        cube = pt.DosCube()
        cube.read(path)
        self.set_dose(cube)

    def set_dose(self, dose):
        self.dose = Dos(self.projection_selector)
        self.dose.cube = dose
