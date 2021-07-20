from matplotlib.projections import register_projection

from pytripgui.canvas_vc.bars.bar import Bar
from pytripgui.canvas_vc.bars.projection_enum import BarProjection


# define new class that inherits from Axes
# class attribute - name - is very important
class CtxBar(Bar):
    name: str = BarProjection.CTX.value

    def __init__(self, fig, rect, **kwargs):
        super().__init__("HU", fig, rect, **kwargs)


# also very important - register new type of projection
# that type is defined by class attribute - name
register_projection(CtxBar)
