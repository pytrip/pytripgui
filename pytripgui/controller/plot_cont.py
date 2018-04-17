import logging

import matplotlib.pyplot as plt
# from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
# import pytrip as pt

logger = logging.getLogger(__name__)


class PlotController(object):
    """
    This class holds all logic for plotting the canvas.
    """
    def __init__(self, model, plot_canvas, ui):
        self._model = model  # hope this is by referece...
        self._pc = plot_canvas
        self._ui = ui

    # @pyqtSlot()
    def update_plot(self):
        """
        Updating plot.
        What has to be plotted could be defined in model/. ?
        And in a seperate file?
        """

        logger.info("Received update_plot signal")

        if self._model.ctx:
            self._plot_ctx()

        self._pc.draw()
        self._pc.move(0, 0)
        self._pc.show()

    def _plot_ctx(self):
        """
        Plot CTX cube
        """
        _m = self._model
        _pm = self._model.plot

        ct_data = _m.ctx.cube[_pm.current_zslice]
        self._pc.axes.imshow(
            ct_data,
            cmap=plt.get_cmap("gray"),
            vmin=-500,
            vmax=2000)

    def _plot_vdx(self):
        """
        """
        pass

    def _plot_dos(self):
        """
        """
        pass

    def _plot_let(self):
        """
        """
        pass

    @staticmethod
    def on_click(event):
        print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
              ('double' if event.dblclick else 'single', event.button,
               event.x, event.y, event.xdata, event.ydata))

    @staticmethod
    def on_mouse_move(event):
        _str = 'move: x=%d, y=%d, xdata=%f, ydata=%f' % (event.x, event.y,
                                                         event.xdata,
                                                         event.ydata)
        print(_str)

        # TODO: how to properly retain reference to ui class?
        # self.ui.statusBar().showMessage(_str)

    @staticmethod
    def on_mouse_wheel(event):
        _str = 'wheel %s: x=%d, y=%d, xdata=%f, ydata=%f' % (event.button,
                                                             event.x, event.y,
                                                             event.xdata,
                                                             event.ydata)
        print(_str)
