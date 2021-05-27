import logging

logger = logging.getLogger(__name__)


class Let:
    def __init__(self, selector):
        self.aspect = 1.0  # aspect ratio of plot

        self.cube = None
        self.data_to_plot = None

        self.min_let = 0
        self.max_let = None
        self.projection_selector = selector

    def prepare_data_to_plot(self):
        if self.cube is None:
            return

        self._set_aspect()
        self.data_to_plot = self.projection_selector.get_projection(self.cube)
        self.data_to_plot[self.data_to_plot <= self.min_let] = self.min_let

    def _set_aspect(self):
        if self.projection_selector.plane == "Transversal":
            self.aspect = 1.0
        else:
            self.aspect = self.cube.slice_distance / self.cube.pixel_size
