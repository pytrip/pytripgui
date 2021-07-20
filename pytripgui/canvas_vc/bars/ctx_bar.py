from matplotlib.projections import register_projection

from pytripgui.canvas_vc.bars.bar import Bar


# define new class that inherits from Axes
# class attribute - name - is very important
class CtxBar(Bar):
    name: str = 'ctx_bar'

    def __init__(self, fig, rect, **kwargs):
        super().__init__(fig, rect, **kwargs)
        self.label = "HU"


# also very important - register new type of projection
# that type is defined by class attribute - name
register_projection(CtxBar)
