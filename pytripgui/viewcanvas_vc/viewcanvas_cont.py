from pytripgui.controller.vdx import Vdx
from pytripgui.viewcanvas_vc.dos import Dos
from pytripgui.viewcanvas_vc.ctx import Ctx
from pytripgui.viewcanvas_vc.let import Let
from pytripgui.viewcanvas_vc.vc_text import ViewCanvasTextCont

import logging
logger = logging.getLogger(__name__)


class ViewCanvasCont(object):
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
        self.figcanvas = ui      # widget for Qt
        self.figure = ui.figure  # placeholder for figure class
        self.axes = ui.axes  # self.axes = plc._ui.vc.axes   # Axes for the figure, i.e. = self.figure.axes
        self.axim_bg = None   # placehodler for AxisImage for background image
        self.axim_ctx = None  # placeholder for AxesImage object returned by imshow() for CTX cube
        self.axim_let = None  # placeholder for AxesImage object returned by imshow() for LETCube
        self.hu_bar = None    # placeholder for Colorbar object returned by matplotlib.colorbar
        self.let_bar = None

        self.zoom = 100.0  # zoom level in percent

        self.plot_bg()

        # Connect events to callbacks
        self._setup_ui_callbacks()

    def _setup_ui_callbacks(self):
        self._ui.set_button_press_callback(self.on_click)
        self._ui.set_scroll_event_callback(self.on_mouse_wheel)

    def on_click(self, event):
        pass

    def on_mouse_wheel(self, event):
        pm = self._model  # plot model

        if event.button == "up":
            pm.projection_selector.next_slice()
        else:
            pm.projection_selector.prev_slice()

        self.update_viewcanvas()

    def update_viewcanvas(self):
        if self._model.ctx:
            Ctx.plot(self)

        if self._model.vdx:
            Vdx.plot(self)

        if self._model.dose:
            self._model.dose.plot(self)

        if self._model.let:
            Let.plot(self)

        # if self._model.cube:  # if any CTX/DOS/LET cube is present, add the text decorators
        #     ViewCanvasTextCont().plot(self)

        self.figcanvas.draw()

    def plot_bg(self):
        import numpy as np
        chessboard_data = np.add.outer(range(32), range(32)) % 2  # chessboard
        self._ui.plot_bg(chessboard_data)



