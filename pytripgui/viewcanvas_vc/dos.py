import numpy as np

import logging
logger = logging.getLogger(__name__)


class Dos(object):
    def __init__(self, config):
        self.aspect = 1.0  # aspect ratio of plot

        self.dos = None  # Placeholder for DosCube() object to be plotted. Only one (!) dose cube can be plotted.
        self.data_to_plot = None
        # self.dose_show = True  # decides whether DosCube is shown or not.
        # self.dose_contour_levels = [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 95.0, 98.0, 100.0, 102.0]
        self.dose_axis = "auto"

        self.dos_scale = None
        self.min_dose = 0
        self.max_dose = None

        self.projection_selector = config

    def prepare_data_to_plot(self):
        if not self.dos:
            return

        self.dos_scale = self.get_proposed_scale()

        if self.dos_scale == "abs":
            factor = 1000 / self.dos.target_dose
        if self.dos_scale == "rel":
            factor = 10

        if not self.dos_scale and self.dos_scale != self.dos_scale:
            self.max_dose = np.amax(self.dos.cube) / factor
        elif not self.dos_scale:
            self.max_dose = np.amax(self.dos.cube) / factor

        dos_data = self.projection_selector.get_projection(self.dos)

        self.data_to_plot = dos_data / float(factor)
        self.data_to_plot[self.data_to_plot <= self.min_dose] = self.min_dose

    def get_proposed_scale(self):
        if self.dos.target_dose <= 0:
            return "rel"
        elif self.dose_axis == "auto" and self.dos.target_dose != 0.0:
            return "abs"
        else:
            return self.dose_axis

    def get_aspect(self):
        if self.config.plane == "Transversal":
            return 1.0
        else:
            return self.dos.slice_distance / self.dos.pixel_size

