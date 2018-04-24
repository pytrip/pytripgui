import logging
# import matplotlib.colors

# import numpy as np
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


class Ctx(object):
    """
    This class holds logic for plotting CTX stuff.
    """

    def __init__(self):
        pass

    @staticmethod
    def plot(plc):
        """
        Plot CTX cube.

        This method adds axim_ctx and _cb to plc.

        :params plc: PlotController

        """

        ctx = plc._model.plot.ctx
        pm = plc._model.plot

        figure = plc.figure
        axes = plc.axes

        if ctx is None:
            logger.debug("DosCube clear")
            if plc.axim_ctx:  # this can happen if LET cube was removed, and DOS cube is remove afterwards.
                plc.axim_ctx.remove()
                plc.axim_ctx = None
            if plc.hu_bar:
                plc.hu_bar.ax.cla()
                plc.hu_bar = None
            return

        logger.debug("CTXCube plot now pm.zslice {}".format(pm.zslice))

        if pm.plane == "Transversal":
            ct_data = ctx.cube[pm.zslice]
            pm.aspect = 1.0
        elif pm.plane == "Sagittal":
            ct_data = ctx.cube[-1:0:-1, -1:0:-1, pm.xslice]
            pm.aspect = ctx.slice_distance / ctx.pixel_size
        elif pm.plane == "Coronal":
            ct_data = ctx.cube[-1:0:-1, pm.yslice, -1:0:-1]
            pm.aspect = ctx.slice_distance / ctx.pixel_size

        # First time the this function is called, the plot is created with the image_show.
        # Once it has been created, retain a reference to the plot for future updates with set_data()
        # which is much faster.
        if not plc.axim_ctx:
            # TODO: shift this layer to the back, so it does not cover DOS and LET.
            plc.axim_ctx = axes.imshow(ct_data,
                                       cmap=plt.get_cmap("gray"),
                                       vmin=pm.contrast_ct[0],
                                       vmax=pm.contrast_ct[1],
                                       aspect=pm.aspect,
                                       zorder=0)
            # plc.axes = plc._ui.vc.axes
        else:
            plc.axim_ctx.set_data(ct_data)

        if pm.plane == "Transversal":
            axes.axis([0, ctx.dimx, ctx.dimy, 0])
        elif pm.plane == "Sagittal":
            axes.axis([0, ctx.dimy, ctx.dimz, 0])
        elif pm.plane == "Coronal":
            axes.axis([0, ctx.dimx, ctx.dimz, 0])

        axes.get_xaxis().set_visible(False)
        axes.get_yaxis().set_visible(False)

        # strictly the contrast bar should be set in the viewer?
        # setup the HU bar:
        if not plc.hu_bar:
            cax = figure.add_axes([0.1, 0.1, 0.03, 0.8])
            cb = figure.colorbar(plc.axim_ctx, cax=cax)
            cb.set_label("HU", color=pm.fg_color, fontsize=pm.cb_fontsize)
            cb.outline.set_edgecolor(pm.bg_color)
            cb.ax.yaxis.set_tick_params(color=pm.fg_color, labelsize=pm.cb_fontsize)
            plt.setp(plt.getp(cb.ax.axes, 'yticklabels'), color=pm.fg_color)
            plc.hu_bar = cb

    @staticmethod
    def change_contrast(plc, contrast):
        """ Sets the contrast if the CT image.
        Bounds are hardcoded to -1000 to 4000, and cannot be exceeded.

        TODO: this could be changed into a @property thing?

        """
        # Cap the HUs to [-1000:4000]
        _hmin = -1000
        _hmax = 4000

        if contrast[0] > _hmax:
            contrast[0] = _hmax
        if contrast[0] < _hmin:
            contrast[0] = _hmin
        if contrast[1] > _hmax:
            contrast[1] = _hmax
        if contrast[1] < _hmin:
            contrast[1] = _hmin

        # Lower bound may not overtake upper bound
        if contrast[0] >= contrast[1]:
            contrast[0] = contrast[1] - 1  # allow -1001 HU for lower bound for plotting reasons

        plc._model.plot.contrast_ct = contrast
        plc.axim_ctx.set_clim(vmin=contrast[0], vmax=contrast[1])
