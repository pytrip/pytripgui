import sys
import argparse
import logging

from PyQt5.QtWidgets import QMainWindow, QApplication

from model.mymodel import MyModel
from controller.main_cont import MainController
from view.main_window import Ui_MainWindow
from view.plot_canvas import PlotCanvas

logger = logging.getLogger(__name__)


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        logger.debug("Setup model")
        self.model = MyModel()
        self.ctrl = MainController(self.model, self)
        self.connect_ui()

        # attach canvas for 2D plots
        m = PlotCanvas(parent=self.ui.tab)
        m = PlotCanvas(parent=self.ui.tab_2)
        m.move(0, 0)

        self.show()

    def connect_ui(self):
        """
        Connect any signals emited from the autogenerated UI to any methods
        of home-made classes.
        """

        # QtDesigner does not really allow custom slot names of different classes.
        # I.e. you may specify "open_ctx" as a slot, but not "ctrl.open_ctx".
        # The only solution I foresee then is simply to manually make all the signal list here.
        # Any better idea?
        #
        self.ui.actionOpen_FooBar.triggered.connect(self.ctrl.open_ctx)
        # ...


def main(args=sys.argv[1:]):
    app = QApplication(sys.argv)

    # setup parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbosity', action='count', help="increase output verbosity", default=0)
    args = parser.parse_args(sys.argv[1:])
    if args.verbosity == 1:
        logging.basicConfig(level=logging.INFO)
    elif args.verbosity > 1:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig()

    logger.debug("Test2")

    w = AppWindow()
    w.show()
    return app.exec_()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
