from pytripgui.canvas_vc.main_plot.images import CtxImage, DoseImage, LetImage


class SlicePlot:
    def __init__(self, axes):
        self.ctx = CtxImage(axes)
        self.dose = DoseImage(axes)
        self.let = LetImage(axes)
