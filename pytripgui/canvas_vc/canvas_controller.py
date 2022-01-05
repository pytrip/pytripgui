import logging

from pytrip import DosCube, LETCube

from pytripgui.canvas_vc.canvas_view import CanvasView
from pytripgui.canvas_vc.gui_state import PatientGuiState
from pytripgui.canvas_vc.plot_model import PlotModel, ProjectionSelector
from pytripgui.plan_executor.patient_model import PatientModel

logger = logging.getLogger(__name__)


class CanvasController:
    """
    This class holds all logic for plotting the canvas, which are shared among subclasses such as Ctx, Vdx etc.
    """
    def __init__(self, model: PlotModel, ui: CanvasView):
        self._model: PlotModel = model
        self._ui: CanvasView = ui

        self._gui_state: PatientGuiState = PatientGuiState()

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
        self._ui.data_sample.update_sample(event)

    def _on_perspective_change(self):
        self._model.projection_selector.plane = self._ui.perspective
        self.clear_view()

        # we need to update max and current values of slider, which depend on perspective
        self._safely_update_slider()

        self._update_canvas_view()
        self._ui.draw()
        self._ui.data_sample.update_perspective(self._model.projection_selector.plane)

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

            self._ui.data_sample.update_mode("Ctx")
            self._ui.data_sample.update_slice_no(self._model.projection_selector.current_slice_no)

        if self._model.dose:
            if self._model.display_filter in ("", "DOS"):
                self._model.display_filter = "DOS"
                self._model.dose.prepare_data_to_plot()
                self._ui.plot_dos(self._model.dose)

                self._ui.data_sample.update_mode("Dose")
                self._ui.data_sample.update_doselet_data(self._model.dose.data_to_plot)

        if self._model.let:
            if self._model.display_filter in ("", "LET"):
                self._model.display_filter = "LET"
                self._model.let.prepare_data_to_plot()
                self._ui.plot_let(self._model.let)

                self._ui.data_sample.update_mode("Let")
                self._ui.data_sample.update_doselet_data(self._model.let.data_to_plot)

    def set_model_data_and_update_view(self, patient: PatientModel, state: PatientGuiState = None):
        """
        Sets patient data (CTX and VDX) to be displayed on canvas,
            restores GUI state (slider height, its position in each plane and ticked VOIs) if present
            and updates whole canvas view.

        If GUI state object is absent
            this method will create new object that holds information about GUI state with default values.

        Without restoring GUI state
            user, after every change of displayed patient, will have to manually:
                - change slider position in each perspective back,
                - tick VOIs back
            which can be frustrating and can be done automatically, as it is by saving and restoring GUI state.

        :param PatientModel patient: object with patient data (CTX and VDX)
        :param PatientGuiState state: object with stored data about user interactions with GUI
        """
        self._ui.clear()

        # GUI state can be None if patient data is added first time
        if state:
            # recreate model with stored positions in each plane
            self._model = PlotModel(state.projection_selector)
            # restore state
            self._gui_state = state
        else:
            # create new model
            self._model = PlotModel(ProjectionSelector())
            # create new gui state object
            self._gui_state = PatientGuiState()
            self._gui_state.projection_selector = self._model.projection_selector

        # load CTX data to plot model
        if patient.ctx:
            self._model.set_ctx(patient.ctx)
            self._model.set_vdx()

        # load VDX data to plot model
        if patient.vdx and patient.vdx.vois:
            self.update_voi_list(patient, state)

        # update data sample with the new cube and last perspective for that cube
        self._ui.data_sample.update_cube(self._model.ctx.cube)
        self._ui.data_sample.update_perspective(self._model.projection_selector.plane)

        # update data to be displayed with loaded data
        self._update_canvas_view()

        self._safely_update_slider()
        self._safely_update_perspective()

        # display updated data
        self._ui.draw()

    def update_voi_list(self, patient: PatientModel, state: PatientGuiState = None):
        """
        Updates the UI element "voi_list" with regards to newly added VOIs to the patient, while preserving its current
        state (ticked checkboxes).
        """
        # fill ui voi list with VOIs from patient
        self._ui.voi_list.fill(patient.vdx.vois, lambda item: item.name, lambda item: item.color)
        if state:
            # restore ticked VOIs
            self._ui.voi_list.tick_checkboxes(state.ticked_voi_list, lambda item: item.name)
            # add ticked VOIs to model
            self._model.vdx.voi_list = self._ui.voi_list.ticked_items()
        # set callback to react on ui voi list updates
        self._ui.voi_list.on_list_item_clicked_callback = self._on_update_voi

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
        self.set_model_data_and_update_view(simulation_results.patient, state)

        self._model.set_ctx(simulation_results.patient.ctx)

        if simulation_item:
            # local fix for pytrip bug
            # in dose header file there is no information about offsets and slice positions
            # so offsets are set to 0 and slice_pos is generated
            # to make plotter work properly with extent we have to have that offsets and slice_pos
            # because extent calculation is based on those values
            # TODO: remove after it is fixed in pytrip
            simulation_item.xoffset = simulation_results.patient.ctx.xoffset
            simulation_item.yoffset = simulation_results.patient.ctx.yoffset
            simulation_item.zoffset = simulation_results.patient.ctx.zoffset
            simulation_item.slice_pos = simulation_results.patient.ctx.slice_pos

        if isinstance(simulation_item, DosCube):
            self._model.set_dose(simulation_item)
            self._model.display_filter = "DOS"
        elif isinstance(simulation_item, LETCube):
            self._model.set_let(simulation_item)
            self._model.display_filter = "LET"

        self._update_canvas_view()
        self._ui.draw()

    def _on_update_voi(self):
        if self._model.vdx:
            self._model.vdx.voi_list = self._ui.voi_list.ticked_items()
            # update gui state object
            self._gui_state.ticked_voi_list = self._model.vdx.voi_list
        self._update_canvas_view()
        self._ui.update()

    def get_gui_state(self) -> PatientGuiState:
        return self._gui_state
