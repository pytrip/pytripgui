from pytripgui.view.qt_gui import UiMainWindow
from pytripgui.view.plot_volhist import VolHist

from pytripgui.canvas_vc.canvas_view import CanvasView

import logging

logger = logging.getLogger(__name__)


class MainView:
    """
    Viewer class for matplotlib 2D plotting widget
    """
    def __init__(self):
        self.ui = UiMainWindow()

        # attach canvas for 2D plots
        self.ui.one_viewcanvas = CanvasView()
        self.ui.tab_Vlayout.addWidget(self.ui.one_viewcanvas.widget())

        self.ui.dvh = VolHist(parent=self.ui.tab_dvh)
        self.ui.lvh = VolHist(parent=self.ui.tab_lvh)

        self.ui.setWindowTitle("PyTRiPGUI")
