from matplotlib import pyplot as plt

from pytripgui.canvas_vc.plotter.images.patient_image_base import PatientImageBase
from pytripgui.canvas_vc.objects.ctx import Ctx


class CtxImage(PatientImageBase):
    def __init__(self, axes):
        super().__init__(axes)
        self._colormap = plt.get_cmap("gray")
        self.zorder = 1

    def plot(self, data: Ctx) -> None:
        # min_x_mm, min_y_mm, min_z_mm = data.cube.indices_to_pos([0, 0, 0])
        # max_x_mm, max_y_mm, max_z_mm = data.cube.indices_to_pos([data.cube.dimx, data.cube.dimy, data.cube.dimz - 1])
        # plane = data.projection_selector.plane
        # if plane == "Transversal":
        #     extent = [min_x_mm, max_x_mm, min_y_mm, max_y_mm]
        # elif plane == "Sagittal":
        #     extent = [min_y_mm, max_y_mm, min_z_mm, max_z_mm]
        # elif plane == "Coronal":
        #     extent = [min_x_mm, max_x_mm, min_z_mm, max_z_mm]
        self._image = self._axes.imshow(data.data_to_plot,
                                        cmap=self._colormap,
                                        vmin=data.contrast_ct[0],
                                        vmax=data.contrast_ct[1],
                                        aspect=data.aspect,
                                        # extent=extent,
                                        # origin='lower',
                                        zorder=self.zorder)
