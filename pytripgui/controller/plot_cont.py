import logging
import pytrip as pt

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

logger = logging.getLogger(__name__)


class PlotController(object):
    """
    This class holds all logic for plotting the canvas.
    """
    def __init__(self, model, fig):
        self.model = model
        self.fig = fig

    @pyqtSlot()
    def update_plot(self):
        """
        Updating plot.
        What has to be plotted could be defined in model/. ? And in a seperate file?
        """

        logger.info("Received update_plot signal")

        # something like this:
        # ct_data = self.model.ctx.cube[63]
        # self.figure.imshow(
        #     ct_data,
        #     cmap=plt.get_cmap("gray"),
        #     vmin=-500,
        #     vmax=2000,
        #     aspect=self.aspect)
        # self.draw()
