from abc import ABC, abstractmethod

from matplotlib.image import AxesImage


class PatientImageBase(ABC):
    def __init__(self, axes):
        self._axes = axes
        self._image = None

    @abstractmethod
    def plot(self, data) -> None:
        pass

    def get(self) -> AxesImage:
        return self._image

    def update(self, data) -> None:
        self._image.set_data(data.data_to_plot)

    def remove(self) -> None:
        self._image.remove()
        self._image = None

    def is_present(self) -> bool:
        return self._image is not None
