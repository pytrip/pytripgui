import sys
import argparse
import logging

from PyQt5.QtWidgets import QApplication

from pytripgui.view.main_view import MainView
from pytripgui.model.main_model import MainModel
from pytripgui.controller.main_cont import MainController

logger = logging.getLogger(__name__)


class AppWindow():
    def __init__(self):

        logger.debug("Setup view")
        self.view = MainView()

        logger.debug("Setup model")
        self.view.ui.model = MainModel(self)    # TODO: remove that 'hack'
        self.view.ui.view = self.view           # TODO: remove that 'hack'

        logger.debug("Setup controller")
        self.ctrl = MainController(self.view.ui)

    def show(self):
        self.view.ui.show()

    def open_files(self, args):
        """
        """
        if args.ctx:
            self.ctrl.open_voxelplan(args.ctx)
        if args.dos:
            self.ctrl.import_dos(args.dos)
        if args.let:
            self.ctrl.import_let(args.let)


def main(args=sys.argv[1:]):
    from pytripgui import __version__ as _ptgv
    from pytrip import __version__ as _ptv
    _vers = "PyTRiP98GUI {} using PyTRiP98 {}".format(_ptgv, _ptv)

    app = QApplication(sys.argv)

    # setup parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbosity', action='count', help="increase output verbosity", default=0)
    parser.add_argument('-V', '--version', action='version', version=(_vers))
    parser.add_argument("--ctx", help="CtxCube", type=str, nargs='?')
    # parser.add_argument("--vdx", help="VdxCube", type=str, nargs='?')
    parser.add_argument("--dos", help="DosCube", type=str, nargs='?')
    parser.add_argument("--let", help="LETCube", type=str, nargs='?')
    args = parser.parse_args(sys.argv[1:])

    # set logging level
    if args.verbosity == 1:
        logging.basicConfig(level=logging.INFO)
    elif args.verbosity > 1:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig()

    w = AppWindow()
    if args:
        w.open_files(args)
    w.view.ui.show()

    return app.exec_()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
