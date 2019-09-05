from pytripgui.controller.vdx import Vdx
from pytripgui.viewcanvas_vc.dos import Dos
from pytripgui.viewcanvas_vc.ctx import Ctx
from pytripgui.viewcanvas_vc.let import Let
from pytripgui.controller.vc_text import ViewCanvasText

import logging
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
        # Outline:
        # The CTX/VDX/DOS/LET plotting area is a single Figure with a single set of Axes, which contains up to three
        # layers of AxesImages. One for CTX, DOS and LET. VDX stuff is plotted directly to the figure.
        self.figcanvas = ui.vc      # widget for Qt
        self.axes = ui.vc.axes  # self.axes = plc._ui.vc.axes   # Axes for the figure, i.e. = self.figure.axes
        self.axim_bg = None   # placehodler for AxisImage for background image
        self.axim_ctx = None  # placeholder for AxesImage object returned by imshow() for CTX cube
        self.axim_dos = None  # placeholder for AxesImage object returned by imshow() for DoseCube
        self.axim_let = None  # placeholder for AxesImage object returned by imshow() for LETCube
        self.hu_bar = None    # placeholder for Colorbar object returned by matplotlib.colorbar
        self.dose_bar = None
        self.let_bar = None

        self.zoom = 100.0  # zoom level in percent

        self.plot_bg()

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

        if self._model.dos_container.dos_list:
            Dos.plot(self)

        if self._model.let_container.let_list:
            Let.plot(self)

        if self._model.plot.cube:  # if any CTX/DOS/LET cube is present, add the text decorators
            ViewCanvasText.plot(self)

        self.figcanvas.draw()
        self.figcanvas.move(0, 0)
        self.figcanvas.show()

    def plot_bg(self):
        """
        (Re)plots the background chessboard image
        """
        # add some default background image
        import numpy as np
        self.chessboard_data = np.add.outer(range(32), range(32)) % 2  # chessboard
        if self.axim_bg:
            self.axim_bg.remove()

        import matplotlib.pyplot as plt
        self.axim_bg = self.axes.imshow(self.chessboard_data, cmap=plt.cm.gray,
                                        vmin=-5, vmax=5,
                                        interpolation='nearest',
                                        extent=self._model.plot.extent,
                                        zorder=0)

    def on_click(self, event):
        """
        Callback for click on canvas.
        """
        _str = '{:s} click: button={:.0f}, x={:.0f}, y={:.0f}, xdata={}, ydata={}'.format(
            'double' if event.dblclick else 'single', event.button, event.x, event.y, event.xdata, event.ydata)
        self._ui.statusbar.showMessage(_str)

        # TODO put up a pop up menu if right clicked on canvas

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
