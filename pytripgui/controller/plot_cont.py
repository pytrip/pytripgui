import logging

from pytripgui.controller.ctx import Ctx
from pytripgui.controller.vdx import Vdx
from pytripgui.controller.dos import Dos
from pytripgui.controller.let import Let
# import matplotlib.pyplot as plt
# from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
# import pytrip as pt

logger = logging.getLogger(__name__)


class PlotController(object):
    """
    This class holds all logic for plotting the canvas, which are shared among subclasses such as Ctx, Vdx etc.
    """

    def __init__(self, model, ui):
        """
        :param MainModel model:
        :param MainWindow ui:
        """
        self._model = model
        self._ui = ui

        # TODO: these maybe do not belong here and could be moved to a viewer?
        self._ims = None  # placeholder for AxesImage object returned by imshow() for CTX cube
        self._dims = None  # placeholder for AxesImage object returned by imshow() for DoseCube
        self._cb = None  # placeholder for Colorbar object returned by matplotlib.colorbar

        # Connect events to callbacks
        self._connect_ui_plot(self._ui.pc)

    def _connect_ui_plot(self, pc):
        """
        Note sure this is the correct place to do this.
        """
        pc.fig.canvas.mpl_connect('button_press_event', self.on_click)
        pc.fig.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        pc.fig.canvas.mpl_connect('scroll_event', self.on_mouse_wheel)
        pc.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

    def update_plot(self):
        """
        Updating plot.
        What has to be plotted could be defined in model/. ?
        And in a seperate file?
        """

        logger.info("Received update_plot signal")

        if self._model.ctx:
            Ctx.plot(self)

        if self._model.vdx:
            Vdx.plot(self)

        if self._model.dos:
            Dos.plot(self)

        if self._model.let:
            Let.plot(self)

        self._ui.pc.draw()
        self._ui.pc.move(0, 0)
        self._ui.pc.show()

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
            'double' if event.dblclick else 'single', event.button, event.x, event.y, event.xdata, event.ydata)
        self._ui.statusbar.showMessage(_str)

        # put up a pop up menu if right clicked on canvas
        if event.button == 3:
            from PyQt5.QtGui import QCursor
            cursor = QCursor()
            pos = cursor.pos()
            self._ui.popMenu.move(pos)
            self._ui.popMenu.show()

    def on_mouse_move(self, event):
        """
        Callback for mouse moved over canvas.
        """
        _str = 'move: x={:.0f}, y={:.0f}, xdata={}, ydata={}'.format(event.x, event.y, event.xdata, event.ydata)
        self._ui.statusbar.showMessage(_str)

    def on_mouse_wheel(self, event):
        """
        Callback for mouse wheel over canvas.
        """
        _str = 'wheel: {:s} x={:.0f}, y={:.0f}, xdata={}, ydata={}'.format(event.button, event.x, event.y, event.xdata,
                                                                           event.ydata)
        self._ui.statusbar.showMessage(_str)

        if not self._model.ctx:
            return

        n_images = self._model.ctx.dimz
        if event.button == "up":
            if self._model.plot.zslice > 0:
                self._model.plot.zslice -= 1
            else:
                self._model.plot.zslice = n_images - 1
        else:
            if self._model.plot.zslice < n_images - 1:
                self._model.plot.zslice += 1
            else:
                self._model.plot.zslice = 0

        self.update_plot()

    def on_key_press(self, event):
        """
        Callback for key pressed while over canvas.
        """
        _str = 'keypress: {} '.format(event)
        print(_str)
