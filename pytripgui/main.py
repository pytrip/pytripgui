import sys
import argparse
import logging

from PyQt5.QtWidgets import QMainWindow, QApplication

from view.main_view import MainView
from model.main_model import MainModel
from controller.main_cont import MainController


logger = logging.getLogger(__name__)


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        logger.debug("Setup views")
        self.view = MainView(self)

        logger.debug("Setup model")
        self.model = MainModel(self)

        logger.debug("Setup controllers")
        self.ctrl = MainController(self)


def main(args=sys.argv[1:]):
    app = QApplication(sys.argv)

    # setup parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbosity', action='count', help="increase output verbosity", default=0)
    args = parser.parse_args(sys.argv[1:])

    # set logging level
    if args.verbosity == 1:
        logging.basicConfig(level=logging.INFO)
    elif args.verbosity > 1:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig()

    w = AppWindow()
    w.show()
    return app.exec_()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
