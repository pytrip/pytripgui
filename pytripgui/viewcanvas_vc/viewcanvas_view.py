from PyQt5.QtWidgets import QSizePolicy
from PyQt5 import QtCore

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

import logging
logger = logging.getLogger(__name__)


class ViewCanvasView(FigureCanvas):
    """
    Viewer class for matplotlib 2D plotting widget
    """

    def __init__(self, parent=None, width=4, height=4, dpi=110):
        """
        Init canvas.
        """
        self.axim_bg = None   # placehodler for AxisImage for background image

        self.figure = Figure(figsize=(width, height), dpi=dpi)

        # Here one can adjust the position of the CTX plot area.
        self.axes = self.figure.add_axes([0, 0, 1, 1])
        self.axes = self.figure.add_subplot(111)

        FigureCanvas.__init__(self, self.figure)

        if parent:
            parent.addWidget(self)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        # next too lines are needed in order to catch keypress events in plot canvas by mpl_connect()
        FigureCanvas.setFocusPolicy(self, QtCore.Qt.ClickFocus)
        FigureCanvas.setFocus(self)

    def set_button_press_callback(self, callback):
        self.figure.canvas.mpl_connect('button_press_event', callback)

    def set_scroll_event_callback(self, callback):
        self.figure.canvas.mpl_connect('scroll_event', callback)

    def set_mouse_motion_callback(self, callback):
        self.figure.canvas.mpl_connect('motion_notify_event', callback)

    def set_key_press_callback(self, callback):
        self.figure.canvas.mpl_connect('key_press_event', callback)

    def plot_bg(self, background):
        extent = [0, 256, 0, 256]  # extention of the axesimage, used for plotting the background image.
        self.axim_bg = self.axes.imshow(
            background, cmap=plt.cm.gray,
            vmin=-5, vmax=5,
            interpolation='nearest',
            extent=extent,
            zorder=0)
