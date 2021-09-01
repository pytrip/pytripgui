import logging

from pytrip import DosCube, LETCube
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

    def _setup_ui_callbacks(self):
        # callback for events emitted by clicking on canvas
        self._ui.set_plotter_click_callback(self._on_click)
        # callback for events emitted by scrolling mouse wheel
        self._ui.set_plotter_wheel_callback(self._on_mouse_wheel)
        # callback for events emitted by changing perspective between transversal, sagittal and coronal
        self._ui.internal_events.on_perspective_change += self._on_perspective_change
        # callback for events emitted by changing position of slider
        self._ui.set_position_changed_callback(self._on_slider_position_change)

    def _on_click(self, event):
        # TODO - add popup menu if needed
        pass

    def _on_mouse_wheel(self, event):
        if event.button == "up":
            self._model.projection_selector.next_slice()
        else:
            self._model.projection_selector.prev_slice()

        # scrolling increments or decrements current slice number which is used to set value on slider
        # and that slider emits event that invokes callback - set_current_slice_no
        self._ui.position = self._model.projection_selector.current_slice_no

    def _on_perspective_change(self):
        self._model.projection_selector.plane = self._ui.perspective
        self.clear_view()

        # we need to update max and current values of slider, which depend on perspective
        self._safely_update_slider()

        self._update_canvas_view()
        self._ui.draw()

    def _on_slider_position_change(self, slice_no):
        self._model.projection_selector.current_slice_no = slice_no
        self._update_canvas_view()
        self._ui.update()

    def clear_view(self):
        self._ui.clear()

    def _update_canvas_view(self):
        if self._model.ctx:
            self._model.ctx.prepare_data_to_plot()
            self._ui.plot_ctx(self._model.ctx)
            if self._model.vdx:
                # TODO this does work, but is not fully reworked yet - POI plotting is deprecated
                self._ui.plot_voi(self._model.vdx)

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

    def set_patient(self, patient, state):
        self._ui.clear()
        if state is None:
            state = ProjectionSelector()
        self._model = PlotModel(state)

        if patient.ctx:
            self._model.set_ctx(patient.ctx)
            self._model.set_vdx()

        if patient.vdx and patient.vdx.vois:
            self._ui.voi_list.event_callback = self._on_update_voi
            self._ui.voi_list.fill(patient.vdx.vois, lambda item: item.name)

        self._update_canvas_view()

        self._safely_update_slider()
        self._safely_update_perspective()

        self._ui.draw()

    def _safely_update_slider(self):
        """
        Safely updates max and current values of ui slider by suppressing position change callback.
        """
        # remove event listener
        self._ui.remove_position_changed_callback(self._on_slider_position_change)
        # set stored height of slider
        self._ui.max_position = self._model.projection_selector.last_slice_no
        # set stored position of slider
        self._ui.position = self._model.projection_selector.current_slice_no
        # add event listener back
        self._ui.set_position_changed_callback(self._on_slider_position_change)

    def _safely_update_perspective(self):
        """
        Safely updates ui perspective by suppressing perspective change callback.
        """
        # remove event listener
        self._ui.internal_events.on_perspective_change -= self._on_perspective_change
        # set stored perspective
        self._ui.perspective = self._model.projection_selector.plane
        # add event listener back
        self._ui.internal_events.on_perspective_change += self._on_perspective_change

    def set_simulation_results(self, simulation_results, simulation_item, state):
        self._ui.clear()
        self.set_patient(simulation_results.patient, state)

        self._model.set_ctx(simulation_results.patient.ctx)

        if simulation_results:
            if simulation_results.dose:
                self._model.set_dose(simulation_results.dose)
            if simulation_results.let:
                self._model.set_let(simulation_results.let)

        if isinstance(simulation_item, DosCube):
            self._model.display_filter = "DOS"
        elif isinstance(simulation_item, LETCube):
            self._model.display_filter = "LET"

        self._update_canvas_view()
        self._ui.draw()

    def _on_update_voi(self):
        if self._model.vdx:
            self._model.vdx.voi_list = self._ui.voi_list.checked_items()
        self._update_canvas_view()
        self._ui.update()

    def get_projection_selector(self):
        return self._model.projection_selector
