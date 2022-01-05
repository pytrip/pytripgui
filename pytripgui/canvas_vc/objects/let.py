import logging

import numpy as np
from pytrip import Cube

from pytripgui.canvas_vc.objects.data_base import PlotDataBase
from pytripgui.canvas_vc.projection_selector import ProjectionSelector

logger = logging.getLogger(__name__)


class Let(PlotDataBase):
    def __init__(self, cube: Cube, selector: ProjectionSelector):
        super().__init__(cube, selector)

        self.min_let = 0
        self.max_let = None

    def prepare_data_to_plot(self):
        if self.cube is None:
            return

        if self.max_let is None:
            self.max_let = np.amax(self.cube.cube)

        self._set_aspect()
        self.data_to_plot = self.projection_selector.get_projection(self.cube)
        self.data_to_plot[self.data_to_plot <= self.min_let] = self.min_let
