import logging

import numpy as np
import matplotlib.pyplot as plt

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

        dos = plc._model.plot.dos
        pm = plc._model.plot

        if dos is None:
            logger.debug("DosCube clear")
            if plc.axim_dos:  # this can happen if LET cube was removed, and DOS cube is remove afterwards.
                plc.axim_dos.remove()
                plc.axim_dos = None
            if plc.dose_bar:
                plc.dose_bar.ax.cla()
                plc.dose_bar = None
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

            if not plc.axim_dos:
                plc.axim_dos = plc._ui.vc.axes.imshow(plot_data,
                                                      cmap=cmap,
                                                      vmax=(pm.max_dose),
                                                      aspect=pm.aspect)
                plc.axes = plc._ui.vc.axes

                # setup colourbar, here called "dose_bar"
                if not plc.dose_bar:
                    cax = plc.axes.figure.add_axes([0.85, 0.1, 0.02, 0.8])
                    cb = plc.axes.figure.colorbar(plc.axim_dos, cax=cax)
                    cb.set_label("Dose", color=pm.fg_color, fontsize=pm.cb_fontsize)
                    cb.outline.set_edgecolor(pm.bg_color)
                    cb.ax.yaxis.set_tick_params(color=pm.fg_color)
                    plt.setp(plt.getp(cb.ax.axes, 'yticklabels'), color=pm.fg_color)
                    cb.ax.yaxis.set_tick_params(color=pm.fg_color, labelsize=pm.cb_fontsize)
                    plc.dose_bar = cb

                    if scale == "abs":
                        plc.dose_bar.set_label("Dose [Gy]")
                    else:
                        plc.dose_bar.set_label("Dose [%]")
            else:
                plc.axim_dos.set_data(plot_data)
