import logging

from pytripgui.model.plot_model import PlotModel

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
        self._ui.set_plotter_click_callback(self.on_click)
        self._ui.set_plotter_wheel_callback(self.on_mouse_wheel)

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

    def set_let_filter(self):
        self._model.display_filter = "LET"
        self._ui.clear()
        self.update_viewcanvas()

    def set_dos_filter(self):
        self._model.display_filter = "DOS"
        self._ui.clear()
        self.update_viewcanvas()

    def set_none_filter(self):
        self._model.display_filter = "NONE"
        self._ui.clear()
        self.update_viewcanvas()

    def on_click(self, event):
        # TODO - add popup menu if needed
        pass

    def on_mouse_wheel(self, event):
        if event.button == "up":
            self._model.projection_selector.next_slice()
        else:
            self._model.projection_selector.prev_slice()

        self.update_viewcanvas()

    def set_current_slice_no(self, slice_no):
        self._model.projection_selector.current_slice_no = slice_no
        self.update_viewcanvas()

    def clear_view(self):
        self._ui.clear()

    def update_viewcanvas(self):
        if self._model.ctx:
            self._model.ctx.prepare_data_to_plot()
            self._ui.plot_ctx(self._model.ctx)

        if self._model.dose:
            if (self._model.display_filter == "") | \
                    (self._model.display_filter == "DOS"):
                self._model.display_filter = "DOS"
                self._model.dose.prepare_data_to_plot()
                self._ui.plot_dos(self._model.dose)

        if self._model.let:
            if (self._model.display_filter == "") | \
                    (self._model.display_filter == "LET"):
                self._model.display_filter = "LET"
                self._model.let.prepare_data_to_plot()
                self._ui.plot_let(self._model.let)

        self._ui.set_slider_position(self._model.projection_selector.current_slice_no,
                                     self._model.projection_selector.last_slice_no)
        # if self._model.vdx:
        #     Vdx.plot(self)
        # if self._model.cube:  # if any CTX/DOS/LET cube is present, add the text decorators
        #     ViewCanvasTextCont().plot(self)

        self._ui.draw()

    def plot_bg(self):
        import numpy as np
        chessboard_data = np.add.outer(range(32), range(32)) % 2  # chessboard
        self._ui.plot_bg(chessboard_data)

    def set_patient(self, patient):
        self._model = PlotModel()
        if patient.ctx:
            self._model.set_ctx(patient.ctx)

        self._ui.set_position_changed_callback(self.set_current_slice_no)
        self.update_viewcanvas()

    def set_simulation_results(self, simulation_results):
        if simulation_results:
            if simulation_results.dose:
                self._model.set_dose(simulation_results.dose)

        if simulation_results:
            if simulation_results.let:
                self._model.set_let(simulation_results.let)

        self.update_viewcanvas()
