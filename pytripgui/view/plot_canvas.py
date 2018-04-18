import logging

from PyQt5.QtWidgets import QSizePolicy
from PyQt5 import QtCore

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# from controller.plot_cont import PlotController

logger = logging.getLogger(__name__)


class PlotCanvas(FigureCanvas):
    """
    Viewer class for matplotlib 2D plotting widget
    """

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        """
        Init canvas.
        """

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        # next too lines are needed in order to catch keypress events in plot canvas by mpl_connect()
        FigureCanvas.setFocusPolicy(self, QtCore.Qt.ClickFocus)
        FigureCanvas.setFocus(self)
