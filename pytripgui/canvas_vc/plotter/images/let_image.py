from matplotlib import pyplot as plt

from pytripgui.canvas_vc.plotter.images.patient_image_base import PatientImageBase
from pytripgui.canvas_vc.objects.let import Let


class LetImage(PatientImageBase):
    def __init__(self, axes):
        super().__init__(axes)
        self._colormap = plt.get_cmap()
        self._colormap._init()
        self._colormap._lut[:, -1] = 0.7
        self._colormap._lut[0, -1] = 0.0
        self.zorder = 10

    def plot(self, data: Let) -> None:
        self._image = self._axes.imshow(data.data_to_plot,
                                        cmap=self._colormap,
                                        vmax=data.max_let,
                                        aspect=data.aspect,
                                        zorder=self.zorder)
