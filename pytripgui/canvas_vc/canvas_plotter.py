from PyQt5 import QtCore
from PyQt5.QtWidgets import QSizePolicy
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from pytripgui.canvas_vc.bars import BarProjection
from pytripgui.canvas_vc.blit_manager import BlitManager
from pytripgui.canvas_vc.main_plot import CoordinateInfo
from pytripgui.canvas_vc.placement_manager import PlacementManager


class CanvasPlotter(FigureCanvas):
    """
    Viewer class for matplotlib 2D plotting widget
    """

    def __init__(self, parent=None, width=16, height=9, dpi=100):
        """
        Init canvas.
        """
        super().__init__()
        # ViewCanvas specific:
        self.text_color = "#33DD33"  # text decorator colour
        self.fg_color = 'white'  # colour for colourbar ticks and labels
        self.bg_color = 'red'  # background colour, i.e. between colourbar and CTX/DOS/LET plot
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

        # plotting fields
        self.figure = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        self.placement_manager = PlacementManager(self.figure)
        self.axes = self.figure.add_subplot(self.placement_manager.get_main_plot_place())
        self.info_axes = None
        self.blit_manager = BlitManager(self)

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
        pass
        # extent = [0, 512, 0, 512]  # extention of the axesimage, used for plotting the background image.
        # self.axim_bg = self.axes.imshow(background,
        #                                 cmap=plt.cm.gray,
        #                                 vmin=-5,
        #                                 vmax=5,
        #                                 interpolation='nearest',
        #                                 extent=extent,
        #                                 zorder=0)

    def remove_dos(self):
        if self.axim_dos:
            self.blit_manager.remove_artist(self.axim_dos)
            self.axim_dos.remove()
            self.axim_dos = None
        if self.dose_bar:
            self.placement_manager.remove_dose_bar()
            self.dose_bar.remove()
            self.dose_bar = None

    def plot_dos(self, dos):
        if not self.axim_dos and dos.max_dose > dos.min_dose:
            self.axim_dos = self.axes.imshow(dos.data_to_plot,
                                             cmap=self.colormap_dose,
                                             vmax=dos.max_dose,
                                             aspect=dos.aspect,
                                             zorder=5)
            self.blit_manager.add_artist(self.axim_dos)
            if not self.dose_bar:
                self.placement_manager.add_dose_bar()
                self._plot_dos_bar(dos)
        else:
            self.axim_dos.set_data(dos.data_to_plot)

    def _plot_dos_bar(self, dos):
        self.dose_bar = self.figure.add_subplot(self.placement_manager.get_dose_bar_place(),
                                                projection=BarProjection.DOS.value)
        self.dose_bar.plot_bar(self.axim_dos, scale=dos.dos_scale)

    def remove_let(self):
        if self.axim_let:
            self.blit_manager.remove_artist(self.axim_let)
            self.axim_let.remove()
            self.axim_let = None
        if self.let_bar:
            self.placement_manager.remove_let_bar()
            self.let_bar.clear_bar()
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
            self.blit_manager.add_artist(self.axim_let)
            if not self.let_bar:
                self.placement_manager.add_let_bar()
                self._plot_let_bar()
        else:
            self.axim_let.set_data(data.data_to_plot)

    def _plot_let_bar(self):
        self.let_bar = self.figure.add_subplot(self.placement_manager.get_let_bar_place(),
                                               projection=BarProjection.LET.value)
        self.let_bar.plot_bar(self.axim_let)

    def remove_ctx(self):
        if self.axim_ctx:
            self.blit_manager.remove_artist(self.axim_ctx)
            self.axim_ctx.remove()
            self.axim_ctx = None
        if self.hu_bar:
            self.placement_manager.remove_ctx_bar()
            self.hu_bar.clear_bar()
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
            self.blit_manager.add_artist(self.axim_ctx)
            if not self.hu_bar:
                self.placement_manager.add_ctx_bar()
                self._plot_hu_bar()
        else:
            self.axim_ctx.set_data(data.data_to_plot)

    def _plot_hu_bar(self):
        self.hu_bar = self.figure.add_subplot(self.placement_manager.get_ctx_bar_place(),
                                              projection=BarProjection.CTX.value)
        self.hu_bar.plot_bar(self.axim_ctx)

    def _plot_coordinate_info(self, data):
        if self.info_axes is None:
            self.info_axes = self.figure.add_subplot(self.placement_manager.get_coord_info_place(),
                                                     projection=CoordinateInfo.name)
            self.blit_manager.add_artist(self.info_axes)

        self.info_axes.update_info(data)

    def update(self):
        self.blit_manager.update()
