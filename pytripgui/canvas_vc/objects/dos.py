from enum import Enum

import numpy as np

import logging

from pytrip import Cube

from pytripgui.canvas_vc.objects.data_base import PlotDataBase
from pytripgui.canvas_vc.projection_selector import ProjectionSelector

logger = logging.getLogger(__name__)


class DoseAxisType(Enum):
    """
    Different type of dose scaling
    """
    auto = 0
    rel = 1
    abs = 2


class Dos(PlotDataBase):
    def __init__(self, cube: Cube, selector: ProjectionSelector):
        super().__init__(cube, selector)

        self.dose_axis = DoseAxisType.auto

        self.dos_scale = None
        self.min_dose = 0
        self.max_dose = None
        self.factor = 1.0
        self._max_dose_from_cube = None

    def prepare_data_to_plot(self):
        if not self.cube:
            return

        if self._max_dose_from_cube is None:
            self._max_dose_from_cube = np.amax(self.cube.cube)

        self.dos_scale = self._get_proposed_scale()
        self._set_aspect()

        if self.dos_scale == DoseAxisType.abs:
            self.factor = 1000.0 / self.cube.target_dose
        elif self.dos_scale == DoseAxisType.rel:
            self.factor = 10.0

        self.max_dose = self._max_dose_from_cube / self.factor

        dos_data = self.projection_selector.get_projection(self.cube)

        self.data_to_plot = dos_data / self.factor
        self.data_to_plot[self.data_to_plot <= self.min_dose] = self.min_dose

    def _get_proposed_scale(self):
        if self.cube.target_dose <= 0:
            return DoseAxisType.rel
        if self.dose_axis == DoseAxisType.auto and self.cube.target_dose != 0.0:
            return DoseAxisType.abs
        return self.dose_axis
