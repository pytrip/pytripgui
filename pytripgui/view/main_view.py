from PyQt5 import QtWidgets, uic

from pytripgui.view.plot_viewcanvas import ViewCanvas
from pytripgui.view.plot_volhist import VolHist

import logging
logger = logging.getLogger(__name__)


class UiMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(UiMainWindow, self).__init__()
        uic.loadUi('../pytripgui/view/main_window.ui', self)


class MainView(object):
    """
    Viewer class for matplotlib 2D plotting widget
    """

    def __init__(self):
        """
        """

        self.ui = UiMainWindow()

        # attach canvas for 2D plots
        self.ui.vc = ViewCanvas(parent=self.ui.tab_view)
        self.ui.dvh = VolHist(parent=self.ui.tab_dvh)
        self.ui.lvh = VolHist(parent=self.ui.tab_lvh)

        self.ui.setWindowTitle("PyTRiPGUI")

        # TODO_move this to proper place
        # create context menu
        self.ui.popMenu = QtWidgets.QMenu()
        self.ui.popMenu.addAction(QtWidgets.QAction('test0'))
        self.ui.popMenu.addAction(QtWidgets.QAction('test1'))
        self.ui.popMenu.addSeparator()
        self.ui.popMenu.addAction(QtWidgets.QAction('test2'))
