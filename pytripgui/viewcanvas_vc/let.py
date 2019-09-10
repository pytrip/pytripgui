import logging

import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


class Let(object):
    """
    This class holds logic for plotting LET stuff.
    """

    def __init__(self):
        pass

    @staticmethod
    def plot(plc):
        """
        Plot the active LET cube.
        :params plc: PlotController

        """
        logger.debug("plot LET cube")

        let = plc._model.plot.let
        pm = plc._model.plot

        if let is None:
            logger.debug("LETCube clear")
            if plc.axim_let:  # this can happen if LET cube was removed, and DOS cube is remove afterwards.
                plc.axim_let.remove()
                plc.axim_let = None
            if plc.let_bar:
                plc.let_bar.ax.cla()
                plc.let_bar = None
            return

        # TODO: this is code duplication from dos.py.
        if pm.plane == "Transversal":
            let_data = let.cube[pm.current_z_slice]
        elif pm.plane == "Sagittal":
            let_data = let.cube[-1:0:-1, -1:0:-1, pm.xslice]
            pm.aspect = let.slice_distance / let.pixel_size
        elif pm.plane == "Coronal":
            let_data = let.cube[-1:0:-1, pm.yslice, -1:0:-1]
            pm.aspect = let.slice_distance / let.pixel_size

        if pm.let_plot == "colorwash":

            cmap = pm.colormap_let
            cmap._init()
            cmap._lut[:, -1] = 0.7
            cmap._lut[0, -1] = 0.0

            let_data[let_data <= pm.min_let] = pm.min_let

            if not plc.axim_let:
                plc.axim_let = plc._ui.axes.imshow(let_data,
                                                      cmap=cmap,
                                                      vmax=(pm.max_let),
                                                      aspect=pm.aspect,
                                                      zorder=10)
                # update the extent actual size in data pixels # TODO, must also be called if plane of view is changed.
                pm.extent = [0, pm.slice_size[0], 0, pm.slice_size[1]]
                plc.plot_bg()

                if not plc.let_bar:
                    # if not pm.let_bar:
                    cax = plc.axes.figure.add_axes([0.92, 0.1, 0.02, 0.8])
                    cb = plc.axes.figure.colorbar(plc.axim_let, cax=cax)
                    # setup some colours
                    cb.set_label("LET (keV/um)", color=pm.fg_color, fontsize=pm.cb_fontsize)
                    cb.outline.set_edgecolor(pm.bg_color)
                    cb.ax.yaxis.set_tick_params(color=pm.fg_color)
                    plt.setp(plt.getp(cb.ax.axes, 'yticklabels'), color=pm.fg_color)
                    cb.ax.yaxis.set_tick_params(color=pm.fg_color, labelsize=pm.cb_fontsize)
                    plc.let_bar = cb
            else:
                plc.axim_let.set_data(let_data)
