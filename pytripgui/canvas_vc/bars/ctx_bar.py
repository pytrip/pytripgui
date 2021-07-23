from matplotlib.projections import register_projection

from pytripgui.canvas_vc.bars.bar import Bar
from pytripgui.canvas_vc.bars.projection_enum import BarProjection


class CtxBar(Bar):
    name: str = BarProjection.CTX.value

    def __init__(self, fig, rect, **kwargs):
        super().__init__(fig, rect, **kwargs)
        self.label = "HU"


register_projection(CtxBar)