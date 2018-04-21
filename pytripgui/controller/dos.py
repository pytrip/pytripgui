import logging

import numpy as np

logger = logging.getLogger(__name__)


class Dos(object):
    """
    This class holds logic for plotting DOS stuff.
    """

    def __init__(self):
        pass

    @staticmethod
    def plot(plc):
        """
        Plot the active dos cube.
        :params plc: PlotController

        """
        logger.debug("plot Dos cube")

        if not plc._model.dos:
            return

        dos = plc._model.dos[-1]  # use the last imported cube for now, selector will be implemented later
        pm = plc._model.plot

        if dos is None:
            # self.clear_dose_view()
            return

        if pm.plane == "Transversal":
            dos_data = dos.cube[pm.zslice]
        elif pm.plane == "Sagittal":
            dos_data = dos.cube[-1:0:-1, -1:0:-1, pm.xslice]
            pm.aspect = dos.slice_distance / dos.pixel_size
        elif pm.plane == "Coronal":
            dos_data = dos.cube[-1:0:-1, pm.yslice, -1:0:-1]
            pm.aspect = dos.slice_distance / dos.pixel_size

        if pm.dose_plot == "colorwash":
            if dos.target_dose <= 0:
                scale = "rel"
            elif pm.dose_axis == "auto" and dos.target_dose is not 0.0:
                scale = "abs"
            else:
                scale = pm.dose_axis
            if scale == "abs":
                factor = 1000 / dos.target_dose
            if scale == "rel":
                factor = 10

            if not pm.dos_scale and pm.dos_scale != scale:
                pm.max_dose = np.amax(dos.cube) / factor
                # self.clear_dose_view()
            elif not pm.dos_scale:
                pm.max_dose = np.amax(dos.cube) / factor

            pm.dos_scale = scale

            cmap = pm.colormap_dose
            cmap._init()
            cmap._lut[:, -1] = 0.7
            cmap._lut[0, -1] = 0.0

            plot_data = dos_data / float(factor)
            plot_data[plot_data <= pm.min_dose] = pm.min_dose

            if plc._dims is None:
                plc._dims = plc._ui.vc.axes.imshow(plot_data, cmap=cmap, vmax=(pm.max_dose), aspect=pm.aspect)
                plc._figure = plc._ui.vc.axes

                if not pm.dose_bar and not pm.let_bar:
                    cax = plc._figure.figure.add_axes([0.9, 0.1, 0.03, 0.8])
                    pm.dose_bar = plc._figure.figure.colorbar(plc._dims, cax=cax)

                if pm.dose_bar:
                    if scale == "abs":
                        pm.dose_bar.set_label("Dose (Gy)")
                    else:
                        pm.dose_bar.set_label("Dose (%)")
            else:
                plc._dims.set_data(plot_data)
