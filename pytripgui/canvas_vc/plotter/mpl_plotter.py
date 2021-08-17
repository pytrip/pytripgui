from PyQt5 import QtCore
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from pytripgui.canvas_vc.plotter.managers import PlottingManager, BlitManager


class MplPlotter(FigureCanvas):
    """
    Viewer class for matplotlib 2D plotting widget
    """
    def __init__(self, parent=None, width=16, height=9, dpi=100):
        """
        Parameters:
        ----------
        parent : type? -- ?

        width : int -- width of created figure

        height : int -- height of created figure

        dpi: int -- dpi of created figure
        """
        super().__init__()
        """
        self.figure has to be initialized before self.blit_manager
        it is so because blit_manager uses figure to do its work - restoring background
        if blit_manager will be created before figure is initialized
        dummy figure will be used and restoring background will work improperly
        """
        self.figure: Figure = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        self.blit_manager: BlitManager = BlitManager(self)
        self.plotting_manager: PlottingManager = PlottingManager(self.figure, self.blit_manager)

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

    def plot_voi(self, vdx):
        self.plotting_manager.plot_voi(vdx)

    def remove_voi(self):
        self.plotting_manager.remove_voi()

    def update(self):
        self.blit_manager.update()
