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

        This method adds _ims and _cb to plc.

        :params plc: PlotController

        """

        ctx = plc._model.ctx
        pm = plc._model.plot

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
        if plc._ims is None:
            plc._ims = plc._ui.vc.axes.imshow(
                ct_data, cmap=plt.get_cmap("gray"), vmin=pm.contrast_ct[0], vmax=pm.contrast_ct[1], aspect=pm.aspect)
            plc._figure = plc._ui.vc.axes
        else:
            plc._ims.set_data(ct_data)

        if pm.plane == "Transversal":
            plc._figure.axis([0, ctx.dimx, ctx.dimy, 0])
        elif pm.plane == "Sagittal":
            plc._figure.axis([0, ctx.dimy, ctx.dimz, 0])
        elif pm.plane == "Coronal":
            plc._figure.axis([0, ctx.dimx, ctx.dimz, 0])

        plc._figure.get_xaxis().set_visible(False)
        plc._figure.get_yaxis().set_visible(False)

        # strictly the contrast bas should be set in the viewer?
        if not plc._cb:
            cax = plc._figure.figure.add_axes([0.1, 0.1, 0.03, 0.8])
            cb = plc._figure.figure.colorbar(plc._ims, cax=cax)
            cb.set_label("HU", color=pm.fg_color)
            cb.outline.set_edgecolor(pm.bg_color)
            cb.ax.yaxis.set_tick_params(color=pm.fg_color, labelsize=pm.cb_fontsize)
            plt.setp(plt.getp(cb.ax.axes, 'yticklabels'), color=pm.fg_color)
            plc._cb = cb

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
        plc._ims.set_clim(vmin=contrast[0], vmax=contrast[1])
