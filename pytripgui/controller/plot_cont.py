import logging

import matplotlib.pyplot as plt
# from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
# import pytrip as pt

logger = logging.getLogger(__name__)


class PlotController(object):
    """
    This class holds all logic for plotting the canvas.
    """
    def __init__(self, model, ui):
        """
        :param MainModel model:
        :param MainWindow ui:
        """
        self._model = model
        self._ui = ui

        # Connect events to callbacks
        self._connect_ui_plot(self._ui.pc)

    def _connect_ui_plot(self, pc):
        """
        Note sure this is the correct place to do this.
        """
        pc.fig.canvas.mpl_connect('button_press_event', self.on_click)
        pc.fig.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        pc.fig.canvas.mpl_connect('scroll_event', self.on_mouse_wheel)

    def update_plot(self):
        """
        Updating plot.
        What has to be plotted could be defined in model/. ?
        And in a seperate file?
        """

        logger.info("Received update_plot signal")

        if self._model.ctx:
            self._plot_ctx()

        self._ui.pc.draw()
        self._ui.pc.move(0, 0)
        self._ui.pc.show()

    def _plot_ctx(self):
        """
        Plot CTX cube
        """
        _m = self._model
        _pm = self._model.plot

        ct_data = _m.ctx.cube[_pm.zslice]
        self._ui.pc.axes.imshow(
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

    def on_click(self, event):
        """
        Callback for click on canvas.
        """
        _str = '{:s} click: button={:.0f}, x={:.0f}, y={:.0f}, xdata={}, ydata={}'.format(
                'double' if event.dblclick else 'single',
                event.button, event.x, event.y, event.xdata, event.ydata)
        self._ui.statusbar.showMessage(_str)

    def on_mouse_move(self, event):
        """
        Callback for mouse moved over canvas.
        """
        _str = 'move: x={:.0f}, y={:.0f}, xdata={}, ydata={}'.format(
                event.x, event.y, event.xdata, event.ydata)
        self._ui.statusbar.showMessage(_str)

    def on_mouse_wheel(self, event):
        """
        Callback for mouse wheel over canvas.
        """
        _str = 'wheel: {:s} x={:.0f}, y={:.0f}, xdata={}, ydata={}'.format(
                event.button, event.x, event.y, event.xdata, event.ydata)
        self._ui.statusbar.showMessage(_str)
