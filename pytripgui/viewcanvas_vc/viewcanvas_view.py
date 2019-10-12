import logging

from PyQt5.QtWidgets import QSizePolicy
from PyQt5 import QtCore
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from pytripgui.view.qt_gui import UiViewCanvas

logger = logging.getLogger(__name__)


class ViewCanvasView:
    def __init__(self, parent=None):
        self._ui = UiViewCanvas(parent)
        self._plotter = ViewCanvasWidget()

        self._ui.vc_layout.addWidget(self._plotter)

        self._ui.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._ui.updateGeometry()

    def widget(self):
        return self._ui

    def show(self):
        self._ui.show()

    def set_transversal_callback(self, fun):
        self._ui.transversal_pushButton.clicked.connect(fun)

    def set_sagittal_callback(self, fun):
        self._ui.sagittal_pushButton.clicked.connect(fun)

    def set_coronal_callback(self, fun):
        self._ui.coronal_pushButton.clicked.connect(fun)

    def set_let_filter_callback(self, fun):
        self._ui.letFilter_pushButton.clicked.connect(fun)

    def set_dos_filter_callback(self, fun):
        self._ui.dosFilter_pushButton.clicked.connect(fun)

    def set_none_filter_callback(self, fun):
        self._ui.noneFilter_pushButton.clicked.connect(fun)

    def set_plotter_click_callback(self, fun):
        self._plotter.set_button_press_callback(fun)

    def set_plotter_wheel_callback(self, fun):
        self._plotter.set_scroll_event_callback(fun)

    def set_position(self, position):
        self._ui.position_label.setText("Position: " + str(position))

    def plot_let(self, data):
        self._plotter.plot_let(data)

    def plot_dos(self, data):
        self._plotter.plot_dos(data)

    def plot_ctx(self, data):
        self._plotter.plot_ctx(data)

    def plot_bg(self, data):
        self._plotter.plot_bg(data)

    def draw(self):
        self._plotter.draw()

    def clear(self):
        self.display_filter = ""
        self._plotter.remove_dos()
        self._plotter.remove_let()
        self._plotter.remove_ctx()


class ViewCanvasWidget(FigureCanvas):
    """
    Viewer class for matplotlib 2D plotting widget
    """

    def __init__(self, parent=None, width=4, height=4, dpi=110):
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
        self.axes = self.figure.add_subplot(111)

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
        self.axim_bg = self.axes.imshow(
            background, cmap=plt.cm.gray,
            vmin=-5, vmax=5,
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
        if not self.axim_dos:
            self.axim_dos = self.axes.imshow(
                dos.data_to_plot,
                cmap=self.colormap_dose,
                vmax=dos.max_dose,
                aspect=dos.aspect,
                zorder=5
            )
            if not self.dose_bar:
                self._plot_dos_bar(dos)
        else:
            self.axim_dos.set_data(dos.data_to_plot)

    def _plot_dos_bar(self, dos):
        cax = self.axes.figure.add_axes([0.85, 0.1, 0.02, 0.8])
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

    def plot_let(self, data):
        if not self.axim_let:
            self.axim_let = self.axes.imshow(
                data.data_to_plot,
                cmap=self.colormap_let,
                vmax=data.max_let,
                aspect=data.aspect,
                zorder=10
            )
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
        if not self.axim_ctx:
            self.axim_ctx = self.axes.imshow(
                data.data_to_plot,
                cmap=self.colormap_ctx,
                vmin=data.contrast_ct[0],
                vmax=data.contrast_ct[1],
                aspect=data.aspect,
                zorder=1
            )
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
