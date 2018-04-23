import logging

import matplotlib.colors
import numpy as np

logger = logging.getLogger(__name__)


class Vdx(object):
    """
    This class holds logic for plotting Vdx stuff.
    """

    def __init__(self):
        pass

    @staticmethod
    def plot(plc):
        """
        Plots the VOIs.
        """
        data = []
        data_closed = []
        pm = plc._model.plot
        vdx = plc._model.vdx
        ctx = plc._model.ctx
        idx = plc._model.plot.zslice

        Vdx.clean_plot(plc)

        for voi in pm.vois:
            _slice = voi.get_slice_at_pos(ctx.slice_to_z(idx + 1))
            if _slice is None:
                continue
            for contour in _slice.contour:
                data.append(np.array(contour.contour) - np.array([ctx.xoffset, ctx.yoffset, 0.0]))
            data_closed.append(contour.contour_closed)

        # get current plane of interest from contours
        data = Vdx.plane_points_idx(data, ctx, plc._model.plot.plane)

        contour_color = np.array(voi.color) / 255.0
        for d, dc in zip(data, data_closed):  # data is list of numpy arrays, holding several contours
            # d has shape (n,3) : represents a single contour, with a list of x,y,z coordinates
            # if n is 1, it means it is a point
            # if n > 1, it means it is a contour
            if d.shape[0] == 1:  # This is a POI, so plot it clearly as a POI
                plc._plot_poi(d[0, 0], d[0, 1], contour_color, voi.name)
            else:  # This is a contour
                # Now check whether contour is open or closed.
                if dc:  # it is closed, we need to repeat the first point at the end
                    xy = np.concatenate((d, [d[0, :]]), axis=0)
                else:
                    xy = d

                plc._figure.plot(xy[:, 0], xy[:, 1], color=contour_color)

    def _plot_poi(plc, x, y, color='#00ff00', legend=''):
        """ Plot a point of interest at x,y
        :params x,y: position in real world CT units
        :params color: colour of the point of interest
        :params legend: name of POI
        """

        size = plc.get_size()  # width and height in pixels
        width = float(size[0]) / plc.zoom * 100.0
        height = float(size[1]) / plc.zoom * 100.0

        # we draw two line segments : one which will underline legend text
        # and other one which will connect the first one with point of interest
        # point coordinates as on the plot below
        #
        #
        #           LEGEND TEXT
        #       ___________________
        #      / (x1,y1)          (x2,y2)
        #     /
        #    /
        #   o (x,y)
        x1 = x + 0.02 * width
        y1 = y - 0.02 * height

        x2 = x1 + 2.0 * len(legend)
        y2 = y1

        # prepare a brighter version of input color, for text and line to point
        if isinstance(color, str):
            _rgb = matplotlib.colors.hex2color(color)
        else:
            _rgb = color
        _hsv = matplotlib.colors.rgb_to_hsv(_rgb)
        _hsv[1] *= 0.5
        bright_color = matplotlib.colors.hsv_to_rgb(_hsv)

        # plot a line (two segments) pointing to dot and underlining legend text
        plc.figure.plot([x, x1, x2], [y, y1, y2], color=bright_color)

        # add the legend text
        plc.figure.text(
            x1,
            y1 - 0.025 * height,
            legend,
            color=bright_color,
            va="top",
            fontsize=7,
            weight='semibold',
            backgroundcolor=(0.0, 0.0, 0.0, 0.8))
        plc.figure.plot(x, y, 'o', color=color)  # plot the dot

    @staticmethod
    def clean_plot(plc):
        """
        Scrub the plot for any lines and text.
        """
        while len(plc._figure.lines) > 0:
            plc._figure.lines.pop(0)
        while len(plc._figure.texts) > 0:
            plc._figure.texts.pop(0)

    @staticmethod
    def plane_points_idx(points, ctx, plane="Transversal"):
        """
        Convert a points in a 3D cube in terms of [mm, mm, mm] to the current plane in terms of [idx,idx]

        :param points:
        :param ctx:
        :param plane:

        TODO: code would be easier to read, if this is split up into two steps. 1) conv. to index, 2) extraction.
        """

        d = points  # why needed? Makes a copy?
        for point in d:
            if plane == "Transversal":
                point[:, 0] /= ctx.pixel_size
                point[:, 1] /= ctx.pixel_size
            elif plane == "Sagittal":
                point[:, 0] = (-point[:, 1] + ctx.pixel_size * ctx.dimx) / ctx.pixel_size
                point[:, 1] = (-point[:, 2] + ctx.slice_distance * ctx.dimz) / ctx.slice_distance
            elif plane == "Coronal":
                point[:, 0] = (-point[:, 0] + ctx.pixel_size * ctx.dimy) / ctx.pixel_size
                point[:, 1] = (-point[:, 2] + ctx.slice_distance * ctx.dimz) / ctx.slice_distance
        return d
