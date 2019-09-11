import logging
import matplotlib.pyplot as plt

from pytripgui.viewcanvas_vc.dos import Dos

logger = logging.getLogger(__name__)


class PlotConfig():
    def __init__(self):
        self.current_x_slice = 50
        self.current_y_slice = 50
        self.current_z_slice = 54

        # "Transversal" (xy)
        # "Sagittal" (yz)
        # "Coronal"  (xz)
        self.plane = "Transversal"


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

        # CTX specific
        self.ctx = None  # cube is also in the main_model, but here this is specific for plotting.
        self.contrast_ct = [-500, 2000]

        # VDX specific
        self.vdx = None  # cube is also in the main_model, but here this is specific for plotting.
        self.vois = []  # list of actual vois to be plotted (this may be fewer than vois in the self.vdx)
        self.plot_vois = True  # whether all vois are plotted at all

        self.config = PlotConfig()
        self.dos = Dos(self.config)

        # LETCube specific
        self.let = None  # Placeholder for LETCube() object to be plotted. Only one (!) LETCube can be plotted.
        self.let_show = True  # decides whether LETCube is shown or not.
        self.let_plot = "colorwash"
        self.colormap_let = plt.get_cmap(None)
        self.min_let = 0
        self.max_let = None

        # Plan specific
        self.plan = None  # Placeholder for plan to be plotted

        # These are used by getters and setters, must come after the other values are initialized.
        self.cube = None
        self.slice_pos_idx = 0
        self.slice_pos_nr = 1
        self.slice_pos_mm = 0.0

    # Here follows primitive getter/setter logic for plot_model. It does not touch anything outside the model.
    @property
    def cube(self):
        """
        Returns current cube based for plotting. Note that either CTX, DOS or LET or all of them can be loaded.
        This function returns either of these, but in the aforementioned order. Returns None if no cube is loaded.
        """
        if self.ctx:
            self._cube = self.ctx
        elif self.dos:
            self._cube = self.dos.dos
        elif self.let:
            self._cube = self.let
        else:
            self._cube = None
        return self._cube

    @cube.setter
    def cube(self, val):
        self._cube = val

    @property
    def slice_pos_idx(self):
        return self._slice_pos_idx

    @slice_pos_idx.setter
    def slice_pos_idx(self, value):
        if not self.slice_size:
            self._slice_pos_idx = 0
            return

        logger.debug("setter: slice_pos_idx: {}".format(value))
        logger.debug("setter: slice_size: {}".format(self.slice_size[2]))

        if value > self.slice_size[2] - 1:
            value = 0
        if value < 0:
            value = self.slice_size[2] - 1

        # remember last X,Y,Z slice (needed if view is switched back and forth)
        if self.plane == "Transversal":
            self.current_z_slice = value
        elif self.plane == "Sagittal":
            self.current_y_slice = value
        elif self.plane == "Coronal":
            self.current_x_slice = value

        self._slice_pos_idx = value

    @property
    def slice_pos_nr(self):
        """
        Current slice position as integer number, starting at 1.
        Plane of view is taken into account.
        """
        return self._slice_pos_idx + 1

    @slice_pos_nr.setter
    def slice_pos_nr(self, value):
        """
        Set current slice position, but let it wrap around last slice, if overshot.
        Slice number starts at 1.
        Plane of view is taken into account.
        """
        self.slice_pos_idx = value - 1
        self._slice_pos_nr = value

    @property
    def slice_pos_mm(self):
        """
        Current slice position in mm.
        Returns 0.0 mm if no data is loaded.
        """
        cube = self.cube
        idx = self.slice_pos_idx

        if not cube:
            return 0.0

        if self.plane == "Transversal":
            _pos = cube.slice_pos[self.slice_pos_idx]
        elif self.plane == "Sagittal":
            _pos = idx * cube.pixel_size + cube.xoffset
        elif self.plane == "Coronal":
            _pos = idx * cube.pixel_size + cube.yoffset

        self._slice_pos_mm = _pos
        return self._slice_pos_mm

    @slice_pos_mm.setter
    def slice_pos_mm(self, val):
        self._slice_pos_mm = val

    @property
    def slice_size(self):
        """
        Returns the size of current slice in number of data pixels, and number of slices, as viewed on screen.
        [width, height, depth] in terms of data pixels (not screen pixels)

        Returns empty list [] if neither DOSCube or CTXCube is loaded
        """
        # use either CTX or DOS cube, in that order as a baseself.
        _c = self.cube

        if not _c:
            return []

        if self.plane == "Transversal":
            width = _c.dimx
            height = _c.dimy
            depth = _c.dimz
        elif self.plane == "Sagittal":
            width = _c.dimx
            height = _c.dimz
            depth = _c.dimy
        elif self.plane == "Coronal":
            width = _c.dimy
            height = _c.dimz
            depth = _c.dimx

        self._slice_size = [width, height, depth]
        return self._slice_size

    @slice_size.setter
    def slice_size(self, val):
        self._slice_size = val
