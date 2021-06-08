import logging

import matplotlib.colors
import numpy as np

logger = logging.getLogger(__name__)


class Vdx:
    """
    This class holds logic for plotting Vdx stuff.
    """
    def __init__(self, projection_selector):
        self.projection_selector = projection_selector
        self.vois = []
        self.ctx = None

    def plot(self, plc):
        """
        Plots the VOIs.
        """
        if not self.vois:
            # there is nothing to plot.
            return

        for voi in self.vois:
            logger.debug("plot() voi:{}".format(voi.name))

            if self.projection_selector.plane == "Transversal":
                _slice = voi.get_slice_at_pos(self.ctx.slice_to_z(self.projection_selector.current_slice_no + 1))
            elif self.projection_selector.plane == "Sagittal":
                _slice = voi.get_2d_slice(voi.sagittal, self.projection_selector.current_slice_no)
            elif self.projection_selector.plane == "Coronal":
                _slice = voi.get_2d_slice(voi.coronal, self.projection_selector.current_slice_no)

            if _slice is None:
                continue

            # for a given VOI, the slice viewed may consist of multiple Contours.
            # contours are in [[x0,y0,z0], [x1,y1,z1], ... [xn,yn,zn]] (mm)
            # they will be transformed and put into <data>
            for _c in _slice.contours:
                data = np.array(_c.contour) - np.array([self.ctx.xoffset, self.ctx.yoffset, 0.0])
                Vdx.plane_points_idx([data], self.ctx)  # this transforms the <data> array
                contour_color = np.array(voi.color) / 255.0

                if _c.contour_closed:
                    xy = np.concatenate((data, [data[0]]), axis=0)
                else:
                    xy = data

                # TODO: what are plotting here? in terms of mm or pixels?
                if _c.number_of_points() == 1:
                    Vdx._plot_poi(plc, xy[0, 0], xy[0, 1], contour_color, voi.name)
                else:
                    plc.axes.plot(xy[:, 0], xy[:, 1], color=contour_color, zorder=15)

    @staticmethod
    def _plot_poi(plc, x, y, color='#00ff00', legend=''):
        """ Plot a point of interest at x,y
        :params x,y: position in real world CT units
        :params color: colour of the point of interest
        :params legend: name of POI
        """

        logger.debug("_plot_poi x,y {} {} mm".format(x, y))

        bbox = plc.axes.get_window_extent().transformed(plc.figure.dpi_scale_trans.inverted())
        width, height = bbox.width * plc.figure.dpi, bbox.height * plc.figure.dpi
        size = [width, height]
        logger.debug("_plot_poi width,height: {} {} pixels".format(width, height))

        # size = plc.get_size()  # width and height in pixels
        width = (float(size[0]) / plc.zoom) * 100.0
        height = (float(size[1]) / plc.zoom) * 100.0

        # TODO: this solution does not scale too well when minimizing maximizing windows.
        # a better solution would be to use absolute pixel values instead.

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
        plc.axes.plot([x, x1, x2], [y, y1, y2], color=bright_color, linestyle=":", lw=1, zorder=15)

        # add the legend text
        plc.axes.text(x1,
                      y1 - 0.025 * height,
                      legend,
                      color=bright_color,
                      va="top",
                      fontsize=7,
                      weight='semibold',
                      backgroundcolor=(0.0, 0.0, 0.0, 0.8),
                      zorder=20)  # zorder higher, so text is always above the lines
        plc.axes.plot(x, y, 'o', color=color, zorder=15)  # plot the dot

    @staticmethod
    def plane_points_idx(points, ctx, plane="Transversal"):
        """
        Convert a points in a 3D cube in terms of [mm, mm, mm] to the current plane in terms of [idx,idx].

        :param points: INPUT: list of points in [[x0,y0,z0],[x1,y1,z1], ...[xn,yn,zn]] (mm) format
                       OUTPUT: list of points pseudo-2D format.
        :param ctx:
        :param plane:

        TODO: code would be easier to read, if this is split up into two steps. 1) conv. to index, 2) extraction.
        """

        ct_pixsize_inv = 1.0 / ctx.pixel_size
        ct_slicedist_inv = 1.0 / ctx.slice_distance

        for point in points:
            if plane == "Transversal":
                point[:, 0] *= ct_pixsize_inv
                point[:, 1] *= ct_pixsize_inv
            elif plane == "Sagittal":
                point[:, 0] = (-point[:, 1] + ctx.pixel_size * ctx.dimx) * ct_pixsize_inv
                point[:, 1] = (-point[:, 2] + ctx.slice_distance * ctx.dimz) * ct_slicedist_inv
            elif plane == "Coronal":
                point[:, 0] = (-point[:, 0] + ctx.pixel_size * ctx.dimy) * ct_pixsize_inv
                point[:, 1] = (-point[:, 2] + ctx.slice_distance * ctx.dimz) * ct_slicedist_inv
