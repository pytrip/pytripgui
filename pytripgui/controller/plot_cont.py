import logging

from pytripgui.controller.ctx import Ctx
from pytripgui.controller.vdx import Vdx
from pytripgui.controller.dos import Dos
from pytripgui.controller.let import Let
from pytripgui.controller.vc_text import ViewCanvasText
# import matplotlib.pyplot as plt
# from PyQt5.QtCore import pyqtSlot
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
        self._lims = None  # placeholder for AxesImage object returned by imshow() for LETCube
        self._cb = None  # placeholder for Colorbar object returned by matplotlib.colorbar

        # initial setup of the ViewCanvas
        rect = ui.vc.fig.patch
        rect.set_facecolor(model.plot.bg_color)

        # Connect events to callbacks
        self._connect_ui_plot(ui.vc)

    def _connect_ui_plot(self, vc):
        """
        Note sure this is the correct place to do this.
        """
        vc.fig.canvas.mpl_connect('button_press_event', self.on_click)
        vc.fig.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        vc.fig.canvas.mpl_connect('scroll_event', self.on_mouse_wheel)
        vc.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

    def update_viewcanvas(self):
        """
        Updating ViewCanvas which holds CTX, VDX, DOS and LET.
        """

        logger.info("Enter update_viewcanvas()")

        if self._model.ctx:
            Ctx.plot(self)

        if self._model.vdx:
            Vdx.plot(self)

        if self._model.dos:
            Dos.plot(self)

        if self._model.let:
            Let.plot(self)

        if self._model.plot.cube:
            ViewCanvasText.plot(self)

        self._ui.vc.draw()
        self._ui.vc.move(0, 0)
        self._ui.vc.show()

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

        pm = self._model.plot  # plot model

        if not pm.cube:
            return

        if event.button == "up":
            pm.slice_pos_idx += 1
        else:
            pm.slice_pos_idx -= 1

        self.update_viewcanvas()

    def on_key_press(self, event):
        """
        Callback for key pressed while over canvas.
        """
        _str = 'keypress: {} '.format(event)
        print(_str)
