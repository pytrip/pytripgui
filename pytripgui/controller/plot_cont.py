import logging

import matplotlib.pyplot as plt
# from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
# import pytrip as pt

logger = logging.getLogger(__name__)


class PlotController(object):
    """
    This class holds all logic for plotting the canvas.
    """
    def __init__(self, model, plot_canvas):
        self.model = model
        self.pc = plot_canvas

    # @pyqtSlot()
    def update_plot(self):
        """
        Updating plot.
        What has to be plotted could be defined in model/. ?
        And in a seperate file?
        """

        logger.info("Received update_plot signal")

        if self.model.ctx:

            ct_data = self.model.ctx.cube[63]
            self.pc.axes.imshow(
                ct_data,
                cmap=plt.get_cmap("gray"),
                vmin=-500,
                vmax=2000)
            self.pc.draw()
            self.pc.move(0, 0)
            self.pc.show()
