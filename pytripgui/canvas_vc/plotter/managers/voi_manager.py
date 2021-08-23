import logging
import random
from copy import deepcopy

import matplotlib.colors
import numpy as np
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from pytrip.vdx import Slice, Voi

from pytripgui.canvas_vc.objects.vdx import Vdx
from pytripgui.canvas_vc.plotter.managers import BlitManager

logger = logging.getLogger(__name__)


class VoiManager:
    def __init__(self, axes: Axes, blit_manager: BlitManager):
        self._axes: Axes = axes
        self._blit_manager: BlitManager = blit_manager
        self._plotted_voi: dict = {}

    def _get_color(self, voi: Voi, i: int):
        # TODO if colors are implemented properly in pytrip - change this method
        i = i % len(voi.colors)
        # color in voi is stored as [a, b, c] where a,b,c are numbers from 0 to 255
        # dividing by 255.0 to have float values from 0.0 to 1.0 to adapt to matplotlib colors
        color = np.array(voi.get_color(i)) / 255.0
        return color

    def plot_voi(self, vdx: Vdx):
        """
        Plots the VOIs.
        """
        # if not vdx.voi_list:
        #     # there is nothing to plot.
        #     return

        # remove VOI that should not be plotted or updated
        voi_names_to_remove = [v for v in self._plotted_voi.keys() if v not in [voi.name for voi in vdx.voi_list]]
        for name in voi_names_to_remove:
            self._remove_all_voi_plots(name)

        for voi in vdx.voi_list:
            logger.debug("plot() voi:{}".format(voi.name))

            # get slice with contours in current plane and position
            current_slice: Slice = self._get_current_slice(vdx, voi)

            # remove VOI plots if it does not exist on current slice
            if current_slice is None:
                if self._plotted_voi.get(voi.name) is not None:
                    self._remove_all_voi_plots(voi.name)
                continue

            contour_color = self._get_color(voi, random.randint(0, len(voi.colors)))
            number_of_contours = len(current_slice.contours)

            # remove redundant voi plots
            # it fixes problem with updating VOIs that change number of contours
            if self._plotted_voi.get(voi.name) is not None and len(self._plotted_voi[voi.name]) != number_of_contours:
                self._remove_all_voi_plots(voi.name)

            # for a given VOI, the slice viewed may consist of multiple Contours.
            for i, _c in enumerate(current_slice.contours):
                # zoffset is set to 0.0 in most cubes, which is wrong
                # because of that fact, next line calculates the zoffset as it should be done in CtxCube
                z_offset = min(vdx.ctx.slice_pos) # slice_pos contains z positions in mm

                # contours are in [[x0,y0,z0], [x1,y1,z1], ... [xn,yn,zn]] (mm), we need to remove offsets
                data = np.array(_c.contour) - np.array([vdx.ctx.xoffset, vdx.ctx.yoffset, z_offset])

                # translating positions in mm into pixel positions
                data_pixels = self._plane_points_idx([data], vdx.ctx, vdx.projection_selector.plane)

                if _c.contour_closed:
                    xy = np.concatenate((data_pixels, [data_pixels[0]]), axis=0)
                else:
                    xy = data_pixels

                # TODO: what are plotting here? in terms of mm or pixels?
                if _c.number_of_points() == 1:
                    # TODO not reworked yet
                    self._plot_poi(xy[0, 0], xy[0, 1], color=contour_color, legend=voi.name)
                else:
                    x, y = self._get_plot_data(vdx, xy)
                    if self._plotted_voi.get(voi.name) is None:
                        self._plotted_voi[voi.name] = []
                    if len(self._plotted_voi[voi.name]) < number_of_contours:
                        (line, ) = self._axes.plot(x, y, color=contour_color, zorder=100)
                        self._plotted_voi[voi.name].append(line)
                        self._blit_manager.add_artist(line)
                    else:
                        line: Line2D = self._plotted_voi[voi.name][i]
                        line.set_data(x, y)

    def _get_plot_data(self, vdx, data) -> ([float], [float]):
        if vdx.projection_selector.plane == "Transversal":
            # "Transversal" (xy)
            return data[:, 0], data[:, 1]
        elif vdx.projection_selector.plane == "Sagittal":
            # "Sagittal" (yz)
            return data[:, 1], data[:, 2]
        elif vdx.projection_selector.plane == "Coronal":
            # "Coronal"  (xz)
            return data[:, 0], data[:, 2]

    def _get_current_slice(self, vdx, voi: Voi) -> Slice:
        _slice: Slice = None
        # get current indices in all planes
        positions_indices = vdx.projection_selector.get_current_slices()
        # transform them into [x, y, z] array
        indices = [positions_indices['Sagittal'], positions_indices['Coronal'], positions_indices['Transversal']]
        # get positions in mm
        positions_mm = voi.cube.indices_to_pos(indices)
        # TODO create enum class that holds all plane strings
        if vdx.projection_selector.plane == "Transversal":
            _slice = voi.get_slice_at_pos(positions_mm[2])
        elif vdx.projection_selector.plane == "Sagittal":
            _slice = voi.get_2d_slice(voi.sagittal, positions_mm[0])
        elif vdx.projection_selector.plane == "Coronal":
            _slice = voi.get_2d_slice(voi.coronal, positions_mm[1])
        return _slice

    def remove_voi(self):
        names = list(self._plotted_voi.keys())
        for name in names:
            self._remove_all_voi_plots(name)

    def _remove_all_voi_plots(self, name):
        for line in self._plotted_voi[name]:
            self._blit_manager.remove_artist(line)
            line.remove()
            del line

        del self._plotted_voi[name]

    def _plane_points_idx(self, points, ctx, plane):
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

        results = deepcopy(points)

        for point, result in zip(points, results):
            if plane == "Transversal":
                result[:, 0] = point[:, 0] * ct_pixsize_inv
                result[:, 1] = point[:, 1] * ct_pixsize_inv
            elif plane == "Sagittal":
                result[:, 1] = (-point[:, 1] + ctx.pixel_size * ctx.dimy) * ct_pixsize_inv
                result[:, 2] = (-point[:, 2] + ctx.slice_distance * ctx.dimz) * ct_slicedist_inv
            elif plane == "Coronal":
                result[:, 0] = (-point[:, 0] + ctx.pixel_size * ctx.dimx) * ct_pixsize_inv
                result[:, 2] = (-point[:, 2] + ctx.slice_distance * ctx.dimz) * ct_slicedist_inv

        return result

    def _plot_poi(self, x, y, color='#00ff00', legend=''):
        # TODO not reworked yet
        """ Plot a point of interest at x,y
        :params x,y: position in real world CT units
        :params color: colour of the point of interest
        :params legend: name of POI
        """

        logger.debug("_plot_poi x,y {} {} mm".format(x, y))

        bbox = self._axes.get_window_extent().transformed(self._axes.figure.dpi_scale_trans.inverted())
        width, height = bbox.width * self._axes.figure.dpi, bbox.height * self._axes.figure.dpi
        # size = [width, height]

        logger.debug("_plot_poi width,height: {} {} pixels".format(width, height))

        # size = plc.get_size()  # width and height in pixels
        # TODO there is no zoom attribute in plc - what was it used for?
        # width = (float(size[0]) / plc.zoom) * 100.0
        # height = (float(size[1]) / plc.zoom) * 100.0

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
        self._axes.plot([x, x1, x2], [y, y1, y2], color=bright_color, linestyle=":", lw=1, zorder=15)

        # add the legend text
        self._axes.text(x1,
                        y1 - 0.025 * height,
                        legend,
                        color=bright_color,
                        va="top",
                        fontsize=7,
                        weight='semibold',
                        backgroundcolor=(0.0, 0.0, 0.0, 0.8),
                        zorder=20)  # zorder higher, so text is always above the lines
        self._axes.plot(x, y, 'o', color=color, zorder=15)  # plot the dot
