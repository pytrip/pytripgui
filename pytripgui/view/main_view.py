import logging

from PyQt5 import QtWidgets

from pytripgui.view.gen.main_window import Ui_MainWindow
from pytripgui.view.plot_viewcanvas import ViewCanvas
from pytripgui.view.plot_volhist import VolHist

logger = logging.getLogger(__name__)


class MainView(object):
    """
    Viewer class for matplotlib 2D plotting widget
    """

    def __init__(self, app):
        """
        """

        self.ui = Ui_MainWindow()
        self.ui.setupUi(app)

        # attach canvas for 2D plots
        self.ui.vc = ViewCanvas(parent=self.ui.tab_view)
        self.ui.dvh = VolHist(parent=self.ui.tab_dvh)
        self.ui.lvh = VolHist(parent=self.ui.tab_lvh)

        app.setWindowTitle("PyTRiPGUI")

        # TODO_move this to proper place
        # create context menu
        self.ui.popMenu = QtWidgets.QMenu(app)
        self.ui.popMenu.addAction(QtWidgets.QAction('test0', app))
        self.ui.popMenu.addAction(QtWidgets.QAction('test1', app))
        self.ui.popMenu.addSeparator()
        self.ui.popMenu.addAction(QtWidgets.QAction('test2', app))
