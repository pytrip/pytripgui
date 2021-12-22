import logging

from pytrip import Cube

from pytripgui.canvas_vc.objects.data_base import PlotDataBase
from pytripgui.canvas_vc.projection_selector import ProjectionSelector

logger = logging.getLogger(__name__)


class Ctx(PlotDataBase):
    def __init__(self, cube: Cube, selector: ProjectionSelector):
        super().__init__(cube, selector)

        self.contrast_ct = [-500, 2000]

    def prepare_data_to_plot(self):
        if self.cube is None:
            return

        self._set_aspect()
        self.data_to_plot = self.projection_selector.get_projection(self.cube)
