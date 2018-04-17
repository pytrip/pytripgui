import logging
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


class PlotModel(object):
    """
    Class for holding attributes for plotting.
    """

    def __init__(self):
        self.current_xslice = 0
        self.current_yslice = 0
        self.current_zslice = 0

        self.contrast_ct = [-100, 400]
        self.vois = []  # list of vois to be plotted
        self.plot_vois = True   # whether all vois are plotted at all

        self.dose_plot = "colorwash"
        self.dosecontour_levels = []

        self.let_plot = "colorwash"
        self.dose_axis = "auto"
        self.colormap_dose = plt.get_cmap(None)
        self.colormap_let = plt.get_cmap(None)

        self.zoom = 100.0
        self.center = [50.0, 50.0]

        self.plan = None  # Placeholder for plan to be plotted
        self.dos = None   # Placeholder for DosCube() object to be plotted
        self.let = None   # Placeholder for LETCube() object to be plotted
