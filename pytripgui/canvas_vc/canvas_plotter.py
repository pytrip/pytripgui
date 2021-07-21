#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtWidgets import QSizePolicy
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class CanvasPlotter(FigureCanvas):
    """
    Viewer class for matplotlib 2D plotting widget
    """
    def __init__(self, parent=None, width=10, height=10, dpi=100):
        """
        Init canvas.
        """
        # ViewCanvas specific:
        self.text_color = "#33DD33"  # text decorator colour
        self.fg_color = 'white'  # colour for colourbar ticks and labels
        self.bg_color = 'black'  # background colour, i.e. between colourbar and CTX/DOS/LET plot
        self.cb_fontsize = 8  # fontsize of colourbar labels
        # Data Specific
        self.axim_bg = None  # placehodler for AxisImage for background image
        # DOS
        self.axim_dos = None  # placeholder for AxesImage object returned by imshow() for DoseCube
        self.dose_bar = None
        self.colormap_dose = plt.get_cmap()
        self.colormap_dose._init()
        self.colormap_dose._lut[:, -1] = 0.7
        self.colormap_dose._lut[0, -1] = 0.0
        # LET
        self.axim_let = None  # placeholder for AxesImage object returned by imshow() for LETCube
        self.let_bar = None
        self.colormap_let = plt.get_cmap()
        self.colormap_let._init()
        self.colormap_let._lut[:, -1] = 0.7
        self.colormap_let._lut[0, -1] = 0.0
        # CTX
        self.axim_ctx = None  # placeholder for AxesImage object returned by imshow() for CTX cube
        self.hu_bar = None  # placeholder for Colorbar object returned by matplotlib.colorbar
        self.colormap_ctx = plt.get_cmap("gray")

        # Figure
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.figure.add_subplot(1, 1, 1)

        self.info_axes = None

        FigureCanvas.__init__(self, self.figure)

        if parent:
            parent.addWidget(self)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        # next too lines are needed in order to catch keypress events in plot canvas by mpl_connect()
        FigureCanvas.setFocusPolicy(self, QtCore.Qt.ClickFocus)
        FigureCanvas.setFocus(self)

        self.figure.patch.set_facecolor(self.bg_color)

    def set_button_press_callback(self, callback):
        self.figure.canvas.mpl_connect('button_press_event', callback)

    def set_scroll_event_callback(self, callback):
        self.figure.canvas.mpl_connect('scroll_event', callback)

    def set_mouse_motion_callback(self, callback):
        self.figure.canvas.mpl_connect('motion_notify_event', callback)

    def set_key_press_callback(self, callback):
        self.figure.canvas.mpl_connect('key_press_event', callback)

    def plot_bg(self, background):
        extent = [0, 512, 0, 512]  # extention of the axesimage, used for plotting the background image.
        self.axim_bg = self.axes.imshow(background,
                                        cmap=plt.cm.gray,
                                        vmin=-5,
                                        vmax=5,
                                        interpolation='nearest',
                                        extent=extent,
                                        zorder=0)

    def remove_dos(self):
        if self.axim_dos:
            self.axim_dos.remove()
            self.axim_dos = None
        if self.dose_bar:
            self.dose_bar.ax.cla()
            self.dose_bar = None

    def plot_dos(self, dos):
        if not self.axim_dos and dos.max_dose > dos.min_dose:
            self.axim_dos = self.axes.imshow(dos.data_to_plot,
                                             cmap=self.colormap_dose,
                                             vmax=dos.max_dose,
                                             aspect=dos.aspect,
                                             zorder=5)
            if not self.dose_bar:
                self._plot_dos_bar(dos)
        else:
            self.axim_dos.set_data(dos.data_to_plot)

    def _plot_dos_bar(self, dos):
        cax = self.axes.figure.add_axes([0.01, 0.1, 0.02, 0.8])
        cb = self.axes.figure.colorbar(self.axim_dos, cax=cax)
        cb.set_label("Dose", color=self.fg_color, fontsize=self.cb_fontsize)
        cb.outline.set_edgecolor(self.bg_color)
        cb.ax.yaxis.set_tick_params(color=self.fg_color)
        plt.setp(plt.getp(cb.ax.axes, 'yticklabels'), color=self.fg_color)
        cb.ax.yaxis.set_tick_params(color=self.fg_color, labelsize=self.cb_fontsize)
        self.dose_bar = cb

        if dos.dos_scale == "abs":
            self.dose_bar.set_label("Dose [Gy]")
        else:
            self.dose_bar.set_label("Dose [%]")

    def remove_let(self):
        if self.axim_let:
            self.axim_let.remove()
            self.axim_let = None
        if self.let_bar:
            self.let_bar.ax.cla()
            self.let_bar = None

    def remove_vois(self):
        while len(self.axes.lines) > 0:
            self.axes.lines.pop(0)
        while len(self.axes.texts) > 0:
            self.axes.texts.pop(0)

    def plot_let(self, data):
        if not self.axim_let:
            self.axim_let = self.axes.imshow(data.data_to_plot,
                                             cmap=self.colormap_let,
                                             vmax=data.max_let,
                                             aspect=data.aspect,
                                             zorder=10)
            if not self.let_bar:
                self._plot_let_bar()
        else:
            self.axim_let.set_data(data.data_to_plot)

    def _plot_let_bar(self):
        cax = self.axes.figure.add_axes([0.85, 0.1, 0.02, 0.8])
        cb = self.axes.figure.colorbar(self.axim_let, cax=cax)
        cb.set_label("LET (keV/um)", color=self.fg_color, fontsize=self.cb_fontsize)
        cb.outline.set_edgecolor(self.bg_color)
        cb.ax.yaxis.set_tick_params(color=self.fg_color)
        plt.setp(plt.getp(cb.ax.axes, 'yticklabels'), color=self.fg_color)
        cb.ax.yaxis.set_tick_params(color=self.fg_color, labelsize=self.cb_fontsize)
        self.let_bar = cb

    def remove_ctx(self):
        if self.axim_ctx:
            self.axim_ctx.remove()
            self.axim_ctx = None
        if self.hu_bar:
            self.hu_bar.ax.cla()
            self.hu_bar = None

    def plot_ctx(self, data):
        self._plot_coordinate_info(data)
        if not self.axim_ctx:
            self.axim_ctx = self.axes.imshow(data.data_to_plot,
                                             cmap=self.colormap_ctx,
                                             vmin=data.contrast_ct[0],
                                             vmax=data.contrast_ct[1],
                                             aspect=data.aspect,
                                             zorder=1)
            if not self.hu_bar:
                self._plot_hu_bar()
        else:
            self.axim_ctx.set_data(data.data_to_plot)

    def _plot_hu_bar(self):
        cax = self.axes.figure.add_axes([0.1, 0.1, 0.03, 0.8])
        cb = self.axes.figure.colorbar(self.axim_ctx, cax=cax)
        cb.set_label("HU", color=self.fg_color, fontsize=self.cb_fontsize)
        cb.outline.set_edgecolor(self.bg_color)
        cb.ax.yaxis.set_tick_params(color=self.fg_color)
        plt.setp(plt.getp(cb.ax.axes, 'yticklabels'), color=self.fg_color)
        cb.ax.yaxis.set_tick_params(color=self.fg_color, labelsize=self.cb_fontsize)
        self.hu_bar = cb

    def _plot_coordinate_info(self, data):
        r = [-1, 1]
        X, Y = np.meshgrid(r, r)
        one = np.ones(4).reshape(2, 2)

        if self.info_axes is None:
            # create place for new plot
            info_axes = self.axes.figure.add_axes([0.8, 0.8, 0.2, 0.2], projection='3d')
            # set plot labels
            info_axes.set_xlabel('x')
            info_axes.set_ylabel('y')
            info_axes.set_zlabel('z')
            # remove grid and axes ticks
            info_axes.grid(False)
            info_axes.set_xticks([])
            info_axes.set_yticks([])
            info_axes.set_zticks([])
            # plot cubic frame
            info_axes.plot_wireframe(X, Y, one, alpha=0.2, color='black')
            info_axes.plot_wireframe(X, Y, -one, alpha=0.2, color='black')
            info_axes.plot_wireframe(X, -one, Y, alpha=0.2, color='black')
            info_axes.plot_wireframe(X, one, Y, alpha=0.2, color='black')
            info_axes.plot_wireframe(one, X, Y, alpha=0.2, color='black')
            info_axes.plot_wireframe(-one, X, Y, alpha=0.2, color='black')
            info_axes.dist = 18
            self.info_axes = info_axes
        else:
            # remove last 3 plots - only planes that show current position of each slice
            del self.info_axes.collections[-3:]

        # get current positions in each plane
        current_slices = data.projection_selector.get_current_slices()
        # get max position for each plane
        last_slices = data.projection_selector.get_last_slices()
        # get current plane type
        current_plane = data.projection_selector.plane

        # plot all three planes
        # rescale from [0...last slice] to [-1...1]
        trans_ones = np.multiply(one, 2 * current_slices['Transversal'] / last_slices['Transversal']) - 1
        # plot full color if this is current plane
        if current_plane == 'Transversal':
            self.info_axes.plot_surface(X, Y, trans_ones, color='g')
        # plot partially transparent if it is not current plane
        else:
            self.info_axes.plot_surface(X, Y, trans_ones, alpha=0.2, color='g')

        sag_ones = np.multiply(one, 2 * current_slices['Sagittal'] / last_slices['Sagittal']) - 1
        if current_plane == 'Sagittal':
            self.info_axes.plot_surface(sag_ones, X, Y, color='r')
        else:
            self.info_axes.plot_surface(sag_ones, X, Y, alpha=0.2, color='r')

        cor_ones = np.multiply(one, 2 * current_slices['Coronal'] / last_slices['Coronal']) - 1
        if current_plane == 'Coronal':
            self.info_axes.plot_surface(X, cor_ones, Y, color='b')
        else:
            self.info_axes.plot_surface(X, cor_ones, Y, alpha=0.2, color='b')
