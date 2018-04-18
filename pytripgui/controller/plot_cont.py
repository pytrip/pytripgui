import logging
import matplotlib.colors

import numpy as np
import matplotlib.pyplot as plt
# from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
# import pytrip as pt

logger = logging.getLogger(__name__)


class PlotController(object):
    """
    This class holds all logic for plotting the canvas.
    """
    def __init__(self, model, ui):
        """
        :param MainModel model:
        :param MainWindow ui:
        """
        self._model = model
        self._ui = ui
        self._ims = None  # placeholder for AxesImage object returned by imshow()

        # Connect events to callbacks
        self._connect_ui_plot(self._ui.pc)

    def _connect_ui_plot(self, pc):
        """
        Note sure this is the correct place to do this.
        """
        pc.fig.canvas.mpl_connect('button_press_event', self.on_click)
        pc.fig.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        pc.fig.canvas.mpl_connect('scroll_event', self.on_mouse_wheel)
        pc.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

    def update_plot(self):
        """
        Updating plot.
        What has to be plotted could be defined in model/. ?
        And in a seperate file?
        """

        logger.info("Received update_plot signal")

        if self._model.ctx:
            self._plot_ctx()

        if self._model.vdx:
            self._plot_vdx()

        self._ui.pc.draw()
        self._ui.pc.move(0, 0)
        self._ui.pc.show()

    def _plot_ctx(self):
        """
        Plot CTX cube.
        """
        _m = self._model
        ctx = self._model.ctx
        _pm = self._model.plot

        if _pm.plane == "Transversal":
            ct_data = ctx.cube[_pm.zslice]
            _pm.aspect = 1.0
        elif _pm.plane == "Sagittal":
            ct_data = ctx.cube[-1:0:-1, -1:0:-1, _pm.xslice]
            _pm.aspect = ctx.slice_distance / ctx.pixel_size
        elif _pm.plane == "Coronal":
            ct_data = ctx.cube[-1:0:-1, _pm.yslice, -1:0:-1]
            _pm.aspect = ctx.slice_distance / ctx.pixel_size

        # First time the this function is called, the plot is created with the image_show.
        # Once it has been created, retain a reference to the plot for future updates with set_data()
        # which is much faster.
        if self._ims is None:
            self._ims = self._ui.pc.axes.imshow(
                        ct_data,
                        cmap=plt.get_cmap("gray"),
                        vmin=_pm.contrast_ct[0],
                        vmax=_pm.contrast_ct[1])
            self._figure = self._ui.pc.axes
        else:
            self._ims.set_data(ct_data)

        if _pm.plane == "Transversal":
            self._figure.axis([0, ctx.dimx, ctx.dimy, 0])
        elif _pm.plane == "Sagittal":
            self._figure.axis([0, ctx.dimy, ctx.dimz, 0])
        elif _pm.plane == "Coronal":
            self._figure.axis([0, ctx.dimx, ctx.dimz, 0])

        self._figure.axes.get_xaxis().set_visible(False)
        self._figure.axes.get_yaxis().set_visible(False)
        if not hasattr(self, "contrast_bar"):
            cax = self._figure.figure.add_axes([0.1, 0.1, 0.03, 0.8])
            self.contrast_bar = self._figure.figure.colorbar(self._ims, cax=cax)

    def _plot_vdx(self):
        """
        Plots the VOIs.
        """
        data = []
        data_closed = []
        vdx = self._model.vdx
        ctx = self._model.ctx
        idx = self._model.plot.zslice

        self.clean_plot()

        for voi in vdx.vois:
            _slice = voi.get_slice_at_pos(ctx.slice_to_z(idx + 1))
            if _slice is None:
                continue
            for contour in _slice.contour:
                data.append(np.array(contour.contour) -
                            np.array([ctx.xoffset, ctx.yoffset, 0.0]))
            data_closed.append(contour.contour_closed)

        plot = True

        # get current plane of interest from contours
        data = self.plane_points_idx(data, ctx, self._model.plot.plane)

        if plot:
            contour_color = np.array(voi.color) / 255.0
            for d, dc in zip(data, data_closed):  # data is list of numpy arrays, holding several contours
                # d has shape (n,3) : represents a single contour, with a list of x,y,z coordinates
                # if n is 1, it means it is a point
                # if n > 1, it means it is a contour
                if d.shape[0] == 1:  # This is a POI, so plot it clearly as a POI
                    self._plot_poi(d[0, 0], d[0, 1], contour_color, voi.name)
                else:  # This is a contour
                    # Now check whether contour is open or closed.
                    if dc:  # it is closed, we need to repeat the first point at the end
                        xy = np.concatenate((d, [d[0, :]]), axis=0)
                    else:
                        xy = d

                    self._figure.plot(xy[:, 0], xy[:, 1], color=contour_color)

    def _plot_poi(self, x, y, color='#00ff00', legend=''):
        """ Plot a point of interest at x,y
        :params x,y: position in real world CT units
        :params color: colour of the point of interest
        :params legend: name of POI
        """

        size = self.get_size()  # width and height in pixels
        width = float(size[0]) / self.zoom * 100.0
        height = float(size[1]) / self.zoom * 100.0

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
        x1 = x + 0.02*width
        y1 = y - 0.02*height

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
        self.figure.plot([x, x1, x2], [y, y1, y2], color=bright_color)

        # add the legend text
        self.figure.text(x1, y1 - 0.025*height,
                         legend,
                         color=bright_color,
                         va="top",
                         fontsize=7,
                         weight='semibold',
                         backgroundcolor=(0.0, 0.0, 0.0, 0.8))
        self.figure.plot(x, y, 'o', color=color)  # plot the dot

    def clean_plot(self):
        """
        Scrub the plot for any lines and text.
        """
        while len(self._figure.lines) > 0:
            self._figure.lines.pop(0)
        while len(self._figure.texts) > 0:
            self._figure.texts.pop(0)

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

    def _plot_dos(self):
        """
        """
        pass

    def _plot_let(self):
        """
        """
        pass

    def on_click(self, event):
        """
        Callback for click on canvas.
        """
        _str = '{:s} click: button={:.0f}, x={:.0f}, y={:.0f}, xdata={}, ydata={}'.format(
                'double' if event.dblclick else 'single',
                event.button, event.x, event.y, event.xdata, event.ydata)
        self._ui.statusbar.showMessage(_str)

    def on_mouse_move(self, event):
        """
        Callback for mouse moved over canvas.
        """
        _str = 'move: x={:.0f}, y={:.0f}, xdata={}, ydata={}'.format(
                event.x, event.y, event.xdata, event.ydata)
        self._ui.statusbar.showMessage(_str)

    def on_mouse_wheel(self, event):
        """
        Callback for mouse wheel over canvas.
        """
        _str = 'wheel: {:s} x={:.0f}, y={:.0f}, xdata={}, ydata={}'.format(
                event.button, event.x, event.y, event.xdata, event.ydata)
        self._ui.statusbar.showMessage(_str)

        if not self._model.ctx:
            return

        n_images = self._model.ctx.dimz
        if event.button == "up":
            if self._model.plot.zslice > 0:
                self._model.plot.zslice -= 1
            else:
                self._model.plot.zslice = n_images - 1
        else:
            if self._model.plot.zslice < n_images - 1:
                self._model.plot.zslice += 1
            else:
                self._model.plot.zslice = 0

        self.update_plot()

    def on_key_press(self, event):
        """
        Callback for key pressed while over canvas.
        """
        _str = 'keypress: {} '.format(event)
        print(_str)
