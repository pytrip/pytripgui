from matplotlib.projections import register_projection

from pytripgui.canvas_vc.bars.bar import Bar
from pytripgui.canvas_vc.bars.projection_enum import BarProjection


class CtxBar(Bar):
    name: str = BarProjection.LET.value

    def __init__(self, fig, rect, **kwargs):
        super().__init__(fig, rect, **kwargs)
        self.label = "LET (keV/um)"


register_projection(CtxBar)
