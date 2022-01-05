from abc import ABC, abstractmethod
from typing import Optional

from pytrip import Cube

from pytripgui.canvas_vc.projection_selector import ProjectionSelector


class PlotDataBase(ABC):
    def __init__(self, cube: Cube, selector: ProjectionSelector):
        self.aspect = 1.0  # aspect ratio of plot

        self.cube: Cube = cube  # placeholder for cube object from pytrip
        self.data_to_plot = None  # placeholder for extracted and prepared data to plot

        self.projection_selector: ProjectionSelector = selector

    @abstractmethod
    def prepare_data_to_plot(self):
        pass

    def _set_aspect(self):
        """
        Set the aspect of the axis scaling, i.e. the ratio of y-unit to x-unit.
        """
        # here we are calculating aspect reverse, because of the way we are accessing data in projection selector
        #   I mean, I guess... something is wrong
        plane = self.projection_selector.plane
        c = self.cube
        vertical_size = 1.0  # some default value
        horizontal_size = 1.0  # some default value
        # "Transversal" (xy)
        if plane == "Transversal":
            vertical_size = c.dimx * c.pixel_size
            horizontal_size = c.dimy * c.pixel_size
        # "Sagittal" (yz)
        elif plane == "Sagittal":
            vertical_size = c.dimy * c.pixel_size
            horizontal_size = c.dimz * c.slice_distance
        # "Coronal" (xz)
        elif plane == "Coronal":
            vertical_size = c.dimx * c.pixel_size
            horizontal_size = c.dimz * c.slice_distance

        self.aspect = vertical_size / horizontal_size
