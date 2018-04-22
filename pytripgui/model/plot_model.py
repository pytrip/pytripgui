import logging
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


class PlotModel(object):
    """
    Class for holding attributes for plotting.
    """

    def __init__(self):
        self.xslice = 0
        self.yslice = 0
        self.zslice = 0

        # current plane to be plotted.
        # May be "Transversal" (xy)
        # "Sagittal" (yz)
        # "Coronal"  (xz)
        self.plane = "Transversal"
        self.aspect = 1.0  # aspect ratio of plot

        self.zoom = 100.0
        self.zoom_levels = [100.0, 110.0, 125.0, 150.0, 200.0, 250.0, 300.0, 400.0]
        self.center = [50.0, 50.0]

        # ViewCanvas specific:
        self.fg_color = 'white'
        self.bg_color = 'black'

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
        self.contrast_ct = [-500, 2000]

        # VDX specific
        self.vois = []  # list of vois to be plotted
        self.plot_vois = True  # whether all vois are plotted at all

        # DosCube specific
        self.dos = None  # Placeholder for DosCube() object to be plotted. Only one (!) dose cube can be plotted.
        self.dose_show = True  # decides whether DosCube is shown or not.
        self.dose_plot = "colorwash"
        self.dose_contour_levels = [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 95.0, 98.0, 100.0, 102.0]
        self.dose_bar = None
        self.dose_axis = "auto"
        self.colormap_dose = plt.get_cmap(None)
        self.dos_scale = None  # TODO: check what this is, change possibly to dose_scale (with 'e')
        self.min_dose = 0
        self.max_dose = None

        # LETCube specific
        self.let = None  # Placeholder for LETCube() object to be plotted. Only one (!) LETCube can be plotted.
        self.let_show = True  # decides whether LETCube is shown or not.
        self.let_plot = "colorwash"
        self.let_bar = None
        self.colormap_let = plt.get_cmap(None)

        # Plan specific
        self.plan = None  # Placeholder for plan to be plotted
