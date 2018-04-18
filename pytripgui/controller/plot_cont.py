import logging

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
        self._ims = None

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
        Plot CTX cube
        """
        _m = self._model
        _pm = self._model.plot

        ct_data = _m.ctx.cube[_pm.zslice]

        # First time the this function is called, the plot is created with the image_show.
        # Once it has been created, retain a reference to the plot for future updates with set_data()
        # which is much faster.
        if self._ims is None:
            self._ims = self._ui.pc.axes.imshow(
                        ct_data,
                        cmap=plt.get_cmap("gray"),
                        vmin=-500,
                        vmax=2000)
            self._figure = self._ui.pc.axes
        else:
            self._ims.set_data(ct_data)

    def _plot_vdx(self):
        """
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
                    pass  # do nothing for now
                    #    self._plot_poi(d[0, 0], d[0, 1], contour_color, voi.name)
                else:  # This is a contour
                    # Now check whether contour is open or closed.
                    if dc:  # it is closed, we need to repeat the first point at the end
                        xy = np.concatenate((d, [d[0, :]]), axis=0)
                    else:
                        xy = d

                    self._figure.plot(xy[:, 0], xy[:, 1], color=contour_color)

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
