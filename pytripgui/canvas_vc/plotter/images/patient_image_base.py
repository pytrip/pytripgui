from abc import ABC, abstractmethod

from matplotlib.image import AxesImage
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
        self._axes = axes
        self._image = None

    @abstractmethod
    def plot(self, data) -> None:
        """
        Plots image from passed data.
        """

    def get(self) -> AxesImage:
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
