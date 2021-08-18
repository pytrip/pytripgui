from matplotlib.projections import register_projection

from pytripgui.canvas_vc.plotter.bars.bar_base import BarBase
from pytripgui.canvas_vc.plotter.bars.projection_enum import BarProjection


class DosBar(BarBase):
    name: str = BarProjection.DOS.value

    def __init__(self, fig, rect, **kwargs):
        super().__init__(fig, rect, **kwargs)
        self.label = "Dose"

    def plot_bar(self, data, **kwargs):
        super().plot_bar(data)
        if kwargs['scale'] == "abs":
            self.bar.set_label("Dose [Gy]")
        else:
            self.bar.set_label("Dose [%]")


register_projection(DosBar)
