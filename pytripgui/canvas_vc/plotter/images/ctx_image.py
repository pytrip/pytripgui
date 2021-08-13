from matplotlib import pyplot as plt

from pytripgui.canvas_vc.plotter.images.patient_image_base import PatientImageBase
from pytripgui.canvas_vc.objects.ctx import Ctx


class CtxImage(PatientImageBase):
    def __init__(self, axes):
        super().__init__(axes)
        self._colormap = plt.get_cmap("gray")
        self.zorder = 1

    def plot(self, data: Ctx) -> None:
        self._image = self._axes.imshow(data.data_to_plot,
                                        cmap=self._colormap,
                                        vmin=data.contrast_ct[0],
                                        vmax=data.contrast_ct[1],
                                        aspect=data.aspect,
                                        zorder=self.zorder)
