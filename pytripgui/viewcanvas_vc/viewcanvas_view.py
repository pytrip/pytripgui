import logging

from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QSizePolicy
from PyQt5 import QtCore

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas



logger = logging.getLogger(__name__)


class ViewCanvasView(FigureCanvas):
    """
    Viewer class for matplotlib 2D plotting widget
    """

    def __init__(self, width=6, height=4, dpi=110):
        """
        Init canvas.
        """

        self.figure = Figure(figsize=(width, height), dpi=dpi)

        # Here one can adjust the position of the CTX plot area.
        self.axes = self.figure.add_axes([1, 0, 1, 1])
        # self.axes = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.figure)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        # next too lines are needed in order to catch keypress events in plot canvas by mpl_connect()
        FigureCanvas.setFocusPolicy(self, QtCore.Qt.ClickFocus)
        FigureCanvas.setFocus(self)
