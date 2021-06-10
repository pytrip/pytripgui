import logging

from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QSizePolicy
from PyQt5 import QtCore

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# from controller.plot_cont import PlotController

logger = logging.getLogger(__name__)


class VolHist(FigureCanvas):
    """
    Viewer class for matplotlib figure for Volume Historgrams
    """
    def __init__(self, parent=None, width=6, height=4, dpi=110):
        """
        Init canvas.
        """

        self.fig = Figure(figsize=(width, height), dpi=dpi)

        # Here one can adjust the position of the CTX plot area.
        # self.axes = self.fig.add_subplot(111)
        self.axes = self.fig.add_axes([0.1, 0.1, 0.85, 0.85])
        self.axes.grid(True)
        self.axes.set_xlabel("(no data)")
        self.axes.set_ylabel("(no data)")

        FigureCanvas.__init__(self, self.fig)

        layout = QVBoxLayout(parent)
        layout.addWidget(self)
        parent.setLayout(layout)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        # next too lines are needed in order to catch keypress events in plot canvas by mpl_connect()
        FigureCanvas.setFocusPolicy(self, QtCore.Qt.ClickFocus)
        FigureCanvas.setFocus(self)
