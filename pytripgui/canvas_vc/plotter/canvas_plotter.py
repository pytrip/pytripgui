from PyQt5 import QtCore
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from pytripgui.canvas_vc.plotter.blit_manager import BlitManager
from pytripgui.canvas_vc.plotter import PlottingManager


class CanvasPlotter(FigureCanvas):
    """
    Viewer class for matplotlib 2D plotting widget
    """
    def __init__(self, parent=None, width=16, height=9, dpi=100):
        """
        Init canvas.
        """
        super().__init__()
        self.figure = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        self.blit_manager = BlitManager(self)
        self.plotting_manager = PlottingManager(self.figure, self.blit_manager)

        FigureCanvas.__init__(self, self.figure)

        if parent:
            parent.addWidget(self)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        # next too lines are needed in order to catch keypress events in plot canvas by mpl_connect()
        FigureCanvas.setFocusPolicy(self, QtCore.Qt.ClickFocus)
        FigureCanvas.setFocus(self)

    def set_button_press_callback(self, callback):
        self.figure.canvas.mpl_connect('button_press_event', callback)

    def set_scroll_event_callback(self, callback):
        self.figure.canvas.mpl_connect('scroll_event', callback)

    def set_mouse_motion_callback(self, callback):
        self.figure.canvas.mpl_connect('motion_notify_event', callback)

    def set_key_press_callback(self, callback):
        self.figure.canvas.mpl_connect('key_press_event', callback)

    def remove_dos(self):
        self.plotting_manager.remove_dos()

    def plot_dos(self, dos):
        self.plotting_manager.plot_dos(dos)

    def remove_let(self):
        self.plotting_manager.remove_let()

    def plot_let(self, data):
        self.plotting_manager.plot_let(data)

    def remove_ctx(self):
        self.plotting_manager.remove_ctx()

    def plot_ctx(self, data):
        self.plotting_manager.plot_ctx(data)

    def update(self):
        self.blit_manager.update()

    def plot_bg(self, background):
        # it is not used, so I commented it for now and raised error for safety
        raise NotImplementedError("plot_bg in canvas_plotter is NOT implemented")
        # extent = [0, 512, 0, 512]  # extention of the axesimage, used for plotting the background image.
        # self.axim_bg = self.axes.imshow(background,
        #                                 cmap=plt.cm.gray,
        #                                 vmin=-5,
        #                                 vmax=5,
        #                                 interpolation='nearest',
        #                                 extent=extent,
        #                                 zorder=0)

    def remove_vois(self):
        # TODO make plotting vois an integral part of plotter, now they are plotted somewhere else
        pass
        # while len(self.axes.lines) > 0:
        #     self.axes.lines.pop(0)
        # while len(self.axes.texts) > 0:
        #     self.axes.texts.pop(0)
