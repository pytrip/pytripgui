from enum import Enum

import numpy as np

import logging

from pytripgui.canvas_vc.objects.data_base import PlotDataBase

logger = logging.getLogger(__name__)


class DoseAxisType(Enum):
    """
    Different type of dose scaling
    """
    auto = 0
    rel = 1
    abs = 2


class Dos(PlotDataBase):
    def __init__(self, selector):
        super().__init__(selector)

        self.dose_axis = DoseAxisType.auto

        self.dos_scale = None
        self.min_dose = 0
        self.max_dose = None

    def prepare_data_to_plot(self):
        if not self.cube:
            return

        self.dos_scale = self._get_proposed_scale()
        self._set_aspect()

        factor = None
        if self.dos_scale == DoseAxisType.abs:
            factor = 1000 / self.cube.target_dose
        if self.dos_scale == DoseAxisType.rel:
            factor = 10

        if factor is not None:
            self.max_dose = np.amax(self.cube.cube) / float(factor)
        else:
            self.max_dose = np.amax(self.cube.cube)

        dos_data = self.projection_selector.get_projection(self.cube)

        self.data_to_plot = dos_data / float(factor)
        self.data_to_plot[self.data_to_plot <= self.min_dose] = self.min_dose

    def _get_proposed_scale(self):
        if self.cube.target_dose <= 0:
            return DoseAxisType.rel
        if self.dose_axis == DoseAxisType.auto and self.cube.target_dose != 0.0:
            return DoseAxisType.abs
        return self.dose_axis
