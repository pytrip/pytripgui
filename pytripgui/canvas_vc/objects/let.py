import logging

from pytripgui.canvas_vc.objects.data_base import PlotDataBase

logger = logging.getLogger(__name__)


class Let(PlotDataBase):
    def __init__(self, selector):
        super().__init__(selector)

        self.min_let = 0
        self.max_let = None

    def prepare_data_to_plot(self):
        if self.cube is None:
            return

        self._set_aspect()
        self.data_to_plot = self.projection_selector.get_projection(self.cube)
        self.data_to_plot[self.data_to_plot <= self.min_let] = self.min_let
