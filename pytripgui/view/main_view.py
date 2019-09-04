from pytripgui.view.qt_gui import UiMainWindow
from PyQt5 import QtWidgets
from pytripgui.view.viewcanvas_widget import ViewCanvasWidget
from pytripgui.view.plot_volhist import VolHist
from PyQt5.QtWidgets import QVBoxLayout

import logging
logger = logging.getLogger(__name__)


class MainView(object):
    """
    Viewer class for matplotlib 2D plotting widget
    """

    def __init__(self):
        self.ui = UiMainWindow()

        # attach canvas for 2D plots
        self.ui.vc = ViewCanvasWidget()
        layout = QVBoxLayout(self.ui.tab_view)
        layout.addWidget(self.ui.vc)

        self.ui.dvh = VolHist(parent=self.ui.tab_dvh)
        self.ui.lvh = VolHist(parent=self.ui.tab_lvh)

        self.ui.setWindowTitle("PyTRiPGUI")
