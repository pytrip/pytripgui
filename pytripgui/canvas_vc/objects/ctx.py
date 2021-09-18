import logging

logger = logging.getLogger(__name__)


class Ctx:
    def __init__(self, selector):
        self.aspect = 1.0  # aspect ratio of plot

        self.cube = None
        self.data_to_plot = None

        self.contrast_ct = [-500, 2000]
        self.projection_selector = selector

    def prepare_data_to_plot(self):
        if self.cube is None:
            return

        self._set_aspect()
        self.data_to_plot = self.projection_selector.get_projection(self.cube)

    def _set_aspect(self):
        if self.projection_selector.plane == "Transversal":
            self.aspect = self.cube.dimx/self.cube.dimy
        elif self.projection_selector.plane == "Sagittal":
            self.aspect = self.cube.dimy*self.cube.pixel_size/(self.cube.dimz*self.cube.slice_distance)
        elif self.projection_selector.plane == "Coronal":
            self.aspect = self.cube.dimx*self.cube.pixel_size/(self.cube.dimz*self.cube.slice_distance)
