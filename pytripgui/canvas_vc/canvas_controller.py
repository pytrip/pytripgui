import logging
import time

from pytripgui.canvas_vc.plot_model import PlotModel, ProjectionSelector

logger = logging.getLogger(__name__)


class CanvasController:
    """
    This class holds all logic for plotting the canvas, which are shared among subclasses such as Ctx, Vdx etc.
    """
    def __init__(self, model, ui):
        self._model = model
        self._ui = ui

        self._setup_ui_callbacks()

        self._ui.internal_events.on_perspective_change += self._perspective_has_changed_callback
        self._ui.internal_events.on_display_filter_change += self._display_filter_has_changed_callback

    def _perspective_has_changed_callback(self):
        self._model.projection_selector.plane = self._ui.perspective
        self.clear_view()
        self.update_canvas_view()
        self._ui.draw()

    def _display_filter_has_changed_callback(self):
        if self._model is None:
            return

        self._model.display_filter = self._ui.display_filter
        self.clear_view()
        self.update_canvas_view()
        self._ui.draw()

    def _setup_ui_callbacks(self):
        self._ui.set_plotter_click_callback(self.on_click)
        self._ui.set_plotter_wheel_callback(self.on_mouse_wheel)

    def on_click(self, event):
        # TODO - add popup menu if needed
        pass

    def on_mouse_wheel(self, event):
        if event.button == "up":
            self._model.projection_selector.next_slice()
        else:
            self._model.projection_selector.prev_slice()

        start = time.time()
        self.update_canvas_view()
        start_draw = time.time()
        self._ui.update()
        # self._ui.draw()
        end_draw = time.time()
        print('Drawing time ', end_draw-start_draw)
        end = time.time()
        print('Whole updating and redrawing operation ', end-start)

    def set_current_slice_no(self, slice_no):
        self._model.projection_selector.current_slice_no = slice_no
        self.update_canvas_view()

    def clear_view(self):
        self._ui.clear()

    def update_canvas_view(self):
        start_update = time.time()
        # self.clear_view()
        self._ui.reset_radiobuttons()
        if self._model.ctx:
            if self._model.vdx:
                self._model.vdx.plot(self._ui._plotter)
            start = time.time()
            self._model.ctx.prepare_data_to_plot()
            end = time.time()
            print('CTX prepraing time ', end-start)
            start = time.time()
            self._ui.plot_ctx(self._model.ctx)
            end = time.time()
            print('CTX plotting time ', end-start)

        if self._model.dose:
            self._ui.enable_dose()
            if (self._model.display_filter == "") | \
                    (self._model.display_filter == "DOS"):
                self._model.display_filter = "DOS"
                start = time.time()
                self._model.dose.prepare_data_to_plot()
                end = time.time()
                print('DOS prepraing time ', end-start)
                start = time.time()
                self._ui.plot_dos(self._model.dose)
                end = time.time()
                print('DOS plotting time ', end-start)

        if self._model.let:
            self._ui.enable_let()
            if (self._model.display_filter == "") | \
                    (self._model.display_filter == "LET"):
                self._model.display_filter = "LET"
                self._model.let.prepare_data_to_plot()
                self._ui.plot_let(self._model.let)

        self._ui.display_filter = self._model.display_filter

        self._ui.max_position = self._model.projection_selector.last_slice_no
        self._ui.position = self._model.projection_selector.current_slice_no
        self._ui.perspective = self._model.projection_selector.plane
        # if self._model.vdx:
        #     Vdx.plot(self)
        # if self._model.cube:  # if any CTX/DOS/LET cube is present, add the text decorators
        #     ViewCanvasTextCont().plot(self)

        end_update = time.time()
        print('Updating canvas time', end_update-start_update)

    def set_patient(self, patient, state):
        self._ui.clear()
        if state is None:
            state = ProjectionSelector()
        self._model = PlotModel(state)

        if patient.ctx:
            self._model.set_ctx(patient.ctx)
            self._model.set_vdx()

        if patient.vdx.vois:
            self._ui.voi_list.event_callback = self._on_update_voi
            self._ui.voi_list.fill(patient.vdx.vois, lambda item: item.name)
            self._on_update_voi()

        self._ui.set_position_changed_callback(self.set_current_slice_no)
        self.update_canvas_view()
        self._ui.draw()

    def set_simulation_results(self, simulation_results, state):
        self.set_patient(simulation_results.patient, None)
        self._ui.clear()
        if state is None:
            state = ProjectionSelector()
        self._model = PlotModel(state)

        self._model.set_ctx(simulation_results.patient.ctx)

        if simulation_results:
            if simulation_results.dose:
                self._model.set_dose(simulation_results.dose)
            if simulation_results.let:
                self._model.set_let(simulation_results.let)
        self.update_canvas_view()
        self._ui.draw()

    def _on_update_voi(self):
        if self._model.vdx:
            self._model.vdx.vois = self._ui.voi_list.checked_items()
        self.update_canvas_view()

    def get_projection_selector(self):
        return self._model.projection_selector
