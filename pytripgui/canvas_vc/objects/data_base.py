from abc import ABC, abstractmethod


class PlotDataBase(ABC):
    def __init__(self, selector):
        self.aspect = 1.0  # aspect ratio of plot

        self.cube = None  # placeholder for cube object from pytrip
        self.data_to_plot = None  # placeholder for extracted and prepared data to plot

        self.projection_selector = selector

    @abstractmethod
    def prepare_data_to_plot(self):
        pass

    def _set_aspect(self):
        if self.projection_selector.plane == "Transversal":
            self.aspect = self.cube.dimx / self.cube.dimy
        elif self.projection_selector.plane == "Sagittal":
            self.aspect = self.cube.dimy * self.cube.pixel_size / (self.cube.dimz * self.cube.slice_distance)
        elif self.projection_selector.plane == "Coronal":
            self.aspect = self.cube.dimx * self.cube.pixel_size / (self.cube.dimz * self.cube.slice_distance)
