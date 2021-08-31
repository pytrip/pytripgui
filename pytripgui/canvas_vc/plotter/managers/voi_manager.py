import logging
from copy import deepcopy
from typing import Optional, Dict, List

import matplotlib.colors
import numpy as np
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from pytrip import CtxCube
from pytrip.vdx import Slice, Voi

from pytripgui.canvas_vc.objects.vdx import Vdx
from pytripgui.canvas_vc.plotter.managers import BlitManager

logger = logging.getLogger(__name__)


class VoiManager:
    def __init__(self, axes: Axes, blit_manager: BlitManager):
        # axes where contours will be plotted
        self._axes: Axes = axes
        # blit manager is needed to add new contour to it, so it can blit them when the time comes
        self._blit_manager: BlitManager = blit_manager
        # dictionary that stores all plotted contours under VOI's name key
        self._plotted_voi: Dict[str, List[Line2D]] = {}

    def plot_voi(self, vdx: Vdx):
        """
        Plots, updates and removes VOIs depending on state of passed argument and VoiManager.
        """

        # remove VOI that should not be plotted or updated
        voi_names_to_remove = [name for name in self._plotted_voi if name not in [voi.name for voi in vdx.voi_list]]
        for name in voi_names_to_remove:
            self._remove_all_voi_plots(name)

        for voi in vdx.voi_list:
            logger.debug("plot() voi:{}".format(voi.name))

            # get slice with contours in current plane and position
            current_slice: Optional[Slice] = self._get_current_slice(vdx, voi)

            if current_slice is None:
                # remove VOI plots if it does not exist on current slice
                if self._plotted_voi.get(voi.name) is not None:
                    self._remove_all_voi_plots(voi.name)
                # continue to the next VOI
                continue

            # randomly pick color defined in pytrip
            contour_color = self._get_color(voi)

            # number of contours to check few conditions
            number_of_contours = len(current_slice.contours)

            # remove redundant voi plots
            # it fixes problem with updating VOIs that change number of contours
            if self._plotted_voi.get(voi.name) is not None and len(self._plotted_voi[voi.name]) != number_of_contours:
                self._remove_all_voi_plots(voi.name)

            # for a given VOI, the slice viewed may consist of multiple Contours.
            for i, _c in enumerate(current_slice.contours):
                # TODO change it after it is fixed in pytrip
                # zoffset is set to 0.0 in most cubes, which is wrong
                # because of that fact, next line calculates the zoffset as it should be done in CtxCube
                # I wonder if substracting slice_distance in needed,
                #   but i think it fits better if you look on plotted contours
                z_offset = min(vdx.ctx.slice_pos) - vdx.ctx.slice_distance  # slice_pos contains z positions in mm

                # contours are in [[x0,y0,z0], [x1,y1,z1], ... [xn,yn,zn]] (mm), we need to remove offsets
                data = np.array(_c.contour) - np.array([vdx.ctx.xoffset, vdx.ctx.yoffset, z_offset])

                # translating positions in mm into pixel positions
                data_pixels = self._plane_points_idx(data, vdx.ctx, vdx.projection_selector.plane)

                # closing contour
                if _c.contour_closed:
                    xy = np.concatenate((data_pixels, [data_pixels[0]]), axis=0)
                else:
                    xy = data_pixels

                # plotting in terms of pixels
                if _c.number_of_points() == 1:
                    # TODO not reworked yet
                    self._plot_poi(xy[0, 0], xy[0, 1], color=contour_color, legend=voi.name)
                else:
                    # get proper "Xs" and "Ys" to plot
                    x, y = self._get_plot_data(vdx, xy)

                    # check if VOI has been plotted, if not, create empty array for contours
                    if self._plotted_voi.get(voi.name) is None:
                        self._plotted_voi[voi.name] = []

                    # check if number of already plotted contour is less than the number of contour in VOI
                    # if it is less, plot current contour and append that plot to array stored under VOI's name
                    if len(self._plotted_voi[voi.name]) < number_of_contours:
                        (line, ) = self._axes.plot(x, y, color=contour_color, zorder=100, scalex=False, scaley=False)
                        self._plotted_voi[voi.name].append(line)
                        self._blit_manager.add_artist(line)

                    # in other case get the line that represent current contour and update it's Xs and Ys
                    else:
                        line: Line2D = self._plotted_voi[voi.name][i]
                        line.set_data(x, y)

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

    def remove_voi(self) -> None:
        names = list(self._plotted_voi.keys())
        for name in names:
            self._remove_all_voi_plots(name)

    def _remove_all_voi_plots(self, name: str) -> None:
        for line in self._plotted_voi[name]:
            self._blit_manager.remove_artist(line)
            line.remove()

        del self._plotted_voi[name]

    @staticmethod
    def _get_color(voi: Voi) -> (float, float, float):
        # color in voi is stored as [a, b, c] where a,b,c are numbers from 0 to 255
        # dividing by 255.0 to have float values from 0.0 to 1.0 to adapt to matplotlib colors
        color = tuple(c / 255.0 for c in voi.get_color())
        return color

    @staticmethod
    def _get_plot_data(vdx: Vdx, data):
        if vdx.projection_selector.plane == "Transversal":
            # "Transversal" (xy)
            return data[:, 0], data[:, 1]
        if vdx.projection_selector.plane == "Sagittal":
            # "Sagittal" (yz)
            return data[:, 1], data[:, 2]
        if vdx.projection_selector.plane == "Coronal":
            # "Coronal"  (xz)
            return data[:, 0], data[:, 2]
        raise ValueError("Wrong plane string in voi manager")

    @staticmethod
    def _get_current_slice(vdx: Vdx, voi: Voi) -> Optional[Slice]:
        _slice: Optional[Slice] = None

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

    @staticmethod
    def _plane_points_idx(points, ctx: CtxCube, plane: str):
        """
        Convert a points in a 3D cube in terms of [mm, mm, mm] to the current plane in terms of [idx,idx].

        :param points: INPUT: list of points in [[x0,y0,z0],[x1,y1,z1], ...[xn,yn,zn]] (mm) format
                       OUTPUT: list of points pseudo-2D format.
        :param ctx: CtxCube
        :param plane: string that represents current plane

        """

        ct_pix_size_inv = 1.0 / ctx.pixel_size
        ct_slice_dist_inv = 1.0 / ctx.slice_distance

        results = deepcopy(points)

        if plane == "Transversal":
            results[:, 0] = points[:, 0] * ct_pix_size_inv
            results[:, 1] = points[:, 1] * ct_pix_size_inv
        elif plane == "Sagittal":
            results[:, 1] = (-points[:, 1] + ctx.pixel_size * ctx.dimy) * ct_pix_size_inv
            results[:, 2] = (-points[:, 2] + ctx.slice_distance * ctx.dimz) * ct_slice_dist_inv
        elif plane == "Coronal":
            results[:, 0] = (-points[:, 0] + ctx.pixel_size * ctx.dimx) * ct_pix_size_inv
            results[:, 2] = (-points[:, 2] + ctx.slice_distance * ctx.dimz) * ct_slice_dist_inv

        return results
