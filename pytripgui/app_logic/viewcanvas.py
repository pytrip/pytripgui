from pytripgui.canvas_vc.canvas_view import CanvasView
from pytripgui.canvas_vc.canvas_controller import CanvasController


class ViewCanvases:
    def __init__(self, parent):
        self.viewcanvas_view = CanvasView(parent)
        self.plot_cont = CanvasController(None, self.viewcanvas_view)

    def widget(self):
        return self.viewcanvas_view.widget()

    def set_patient(self, patient, state=None):
        self.plot_cont.set_model_data_and_update_view(patient, state)

    def set_simulation_results(self, simulation_results, simulation_item, state=None):
        self.plot_cont.set_simulation_results(simulation_results, simulation_item, state)

    def update_voi_list(self, patient, state=None):
        self.plot_cont.update_voi_list(patient, state)

    def get_gui_state(self):
        return self.plot_cont.get_gui_state()
