import argparse
import logging
import sys

from PyQt5.QtWidgets import QApplication

from pytripgui.main_window_qt_vc.main_window_view import MainWindowQtView
from pytripgui.main_window_qt_vc.main_window_cont import MainWindowController
from pytripgui.model.main_model import MainModel

logger = logging.getLogger(__name__)


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    from pytripgui import __version__ as _ptgv
    from pytrip import __version__ as _ptv
    _vers = "PyTRiP98GUI {} using PyTRiP98 {}".format(_ptgv, _ptv)

    # setup parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbosity', action='count', help="increase output verbosity", default=0)
    parser.add_argument('-V', '--version', action='version', version=_vers)
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

    # all these objects need to be saved as variables, otherwise they will be garbage collected before app execution
    app = QApplication(sys.argv)
    view = MainWindowQtView()
    model = MainModel()
    controller = MainWindowController(model, view)

    view.show()

    if controller:
        logger.debug("MainWindowController is active to serve its callbacks.")

    return app.exec_()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
