import logging
logger = logging.getLogger(__name__)


class ViewCanvasCont(object):
    """
    This class holds all logic for plotting the canvas, which are shared among subclasses such as Ctx, Vdx etc.
    """

    def __init__(self, model, ui):
        self._model = model
        self._ui = ui

        self.plot_bg()

        self._setup_ui_callbacks()

    def _setup_ui_callbacks(self):
        # plotter
        self._ui.plotter.set_button_press_callback(self.on_click)
        self._ui.plotter.set_scroll_event_callback(self.on_mouse_wheel)
        # ui
        self._ui.set_transversal_callback(self.set_transversal_view)
        self._ui.set_sagittal_callback(self.set_sagittal_view)
        self._ui.set_coronal_callback(self.set_coronal_view)

    def set_transversal_view(self):
        self._model.projection_selector.plane = "Transversal"
        self.clear_view()
        self.update_viewcanvas()

    def set_sagittal_view(self):
        self._model.projection_selector.plane = "Sagittal"
        self.clear_view()
        self.update_viewcanvas()

    def set_coronal_view(self):
        self._model.projection_selector.plane = "Coronal"
        self.clear_view()
        self.update_viewcanvas()


    def on_click(self, event):
        # TODO - add popup menu if needed
        pass

    def on_mouse_wheel(self, event):
        pm = self._model  # plot model

        if event.button == "up":
            pm.projection_selector.next_slice()
        else:
            pm.projection_selector.prev_slice()

        self.update_viewcanvas()

    def clear_view(self):
        self._ui.plotter.clear()

    def update_viewcanvas(self):
        if self._model.ctx:
            self._model.ctx.prepare_data_to_plot()
            self._ui.plotter.plot_ctx(self._model.ctx)

        # if self._model.vdx:
        #     Vdx.plot(self)

        if self._model.dose:
            self._model.dose.prepare_data_to_plot()
            self._ui.plotter.plot_dos(self._model.dose)

        if self._model.let:
            self._model.let.prepare_data_to_plot()
            self._ui.plotter.plot_let(self._model.let)

        # if self._model.cube:  # if any CTX/DOS/LET cube is present, add the text decorators
        #     ViewCanvasTextCont().plot(self)

        self._ui.plotter.draw()

    def plot_bg(self):
        import numpy as np
        chessboard_data = np.add.outer(range(32), range(32)) % 2  # chessboard
        self._ui.plotter.plot_bg(chessboard_data)
