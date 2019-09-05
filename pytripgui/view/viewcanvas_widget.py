from PyQt5.QtWidgets import QSizePolicy
from PyQt5 import QtCore

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import logging
logger = logging.getLogger(__name__)


class ViewCanvasWidget(FigureCanvas):

    def __init__(self, width=6, height=4, dpi=110, bg_color = 'black'):
        self.fig = Figure(figsize=(width, height), dpi=dpi)

        # Here one can adjust the position of the CTX plot area.
        self.axes = self.fig.add_axes([0, 0, 1, 1])

        FigureCanvas.__init__(self, self.fig)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        # next too lines are needed in order to catch keypress events in plot canvas by mpl_connect()
        FigureCanvas.setFocusPolicy(self, QtCore.Qt.ClickFocus)
        FigureCanvas.setFocus(self)

        # initial setup of the ViewCanvas
        self.fig.patch.set_facecolor(bg_color)