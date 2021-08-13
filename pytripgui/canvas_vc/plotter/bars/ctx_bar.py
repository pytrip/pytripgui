from matplotlib.projections import register_projection

from pytripgui.canvas_vc.plotter.bars.bar_base import BarBase
from pytripgui.canvas_vc.plotter.bars.projection_enum import BarProjection


class CtxBar(BarBase):
    name: str = BarProjection.CTX.value

    def __init__(self, fig, rect, **kwargs):
        super().__init__(fig, rect, **kwargs)
        self.label = "HU"


register_projection(CtxBar)
