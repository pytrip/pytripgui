from abc import ABC, abstractmethod
from typing import Optional

from matplotlib.axes import Axes
from matplotlib.image import AxesImage
from pytrip import Cube

from pytripgui.canvas_vc.objects.data_base import PlotDataBase

"""
This class and its subclasses were made to remove extra responsibility from mpl_plotter.
It has methods that allow to show image, check if it is shown, update and remove it.
Greatly removes code duplicates and hides information how images are made.
"""


class PatientImageBase(ABC):
    """
    Abstract base class that holds CRUD-like methods common for all shown images

    Method plot(data) must be implemented in subclasses, because it strongly depends on type of shown image
    """

    def __init__(self, axes):
        """
        Parameters
        ----------
        axes : Axes -- axes on which images will be shown
        """
        self._axes: Axes = axes
        self._image: Optional[AxesImage] = None

    @abstractmethod
    def plot(self, data) -> None:
        """
        Plots image from passed data.
        """

    def get(self) -> Optional[AxesImage]:
        """
        Returns plotted image.
        """
        return self._image

    def update(self, data) -> None:
        """
        Updates data in plotted image.
        """
        self._image.set_data(data.data_to_plot)

    def remove(self) -> None:
        """
        Removes image from axes.
        """
        self._image.remove()
        self._image = None

    def is_present(self) -> bool:
        """
        Returns True if image is present and False if image is absent
        """
        return self._image is not None

    def calculate_extent(self, data: PlotDataBase):
        """
        Returns extent for passed data.
        """
        # get minimal X, Y and Z coordinates
        cube: Cube = data.cube
        min_x_mm, min_y_mm, min_z_mm = cube.indices_to_pos([0, 0, 0])
        # get maximal X, Y and Z coordinates
        # 'data.cube.dimz - 1' is described in https://github.com/pytrip/pytrip/issues/592
        max_x_mm, max_y_mm, max_z_mm = cube.indices_to_pos([cube.dimx, cube.dimy, cube.dimz - 1])
        plane = data.projection_selector.plane
        # depending on plane, return proper list those above
        # extent = [horizontal_min, horizontal_max, vertical_min, vertical_max]
        # "Transversal" (xy)
        if plane == "Transversal":
            return min_x_mm, max_x_mm, min_y_mm, max_y_mm
        # "Sagittal" (yz)
        if plane == "Sagittal":
            return min_y_mm, max_y_mm, min_z_mm, max_z_mm
        # "Coronal" (xz)
        if plane == "Coronal":
            return min_x_mm, max_x_mm, min_z_mm, max_z_mm

        raise ValueError("Wrong plane string - " + plane + " - in " + type(self).__name__)
