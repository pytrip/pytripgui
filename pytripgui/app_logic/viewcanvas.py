from pytripgui.viewcanvas_vc.viewcanvas_view import ViewCanvasView
from pytripgui.viewcanvas_vc.viewcanvas_cont import ViewCanvasCont


class ViewCanvases:
    def __init__(self):
        self.viewcanvas_view = ViewCanvasView()
        self.plot_cont = ViewCanvasCont(None, self.viewcanvas_view)

    def widget(self):
        return self.viewcanvas_view.widget()

    def set_patient(self, patient, state=None):
        return self.plot_cont.set_patient(patient, state)

    def set_simulation_results(self, simulation_results, state=None):
        return self.plot_cont.set_simulation_results(simulation_results, state)
