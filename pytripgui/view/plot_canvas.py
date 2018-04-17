import logging

from PyQt5.QtWidgets import QSizePolicy

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

logger = logging.getLogger(__name__)


class PlotCanvas(FigureCanvas):
    """
    Viewer class for matplotlib 2D plotting widget
    """

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        """
        Init canvas.
        """

        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def test_plot(self):  # this to be moved to controller
        """
        Some random data to be filled into the plot.
        """
        import random
        data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        ax.set_title('PyQt Matplotlib Example')
        self.draw()
