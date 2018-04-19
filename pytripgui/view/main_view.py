import logging

from PyQt5 import QtGui, QtWidgets

from view.main_window import Ui_MainWindow
from view.plot_canvas import PlotCanvas

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
        self.ui.pc = PlotCanvas(parent=self.ui.tab)

        app.setWindowTitle("PyTRiPGUI")

        # TODO_move this to proper place
        # create context menu
        self.ui.popMenu = QtWidgets.QMenu(app)
        self.ui.popMenu.addAction(QtWidgets.QAction('test0', app))
        self.ui.popMenu.addAction(QtWidgets.QAction('test1', app))
        self.ui.popMenu.addSeparator()
        self.ui.popMenu.addAction(QtWidgets.QAction('test2', app))
