from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from pytripgui.view.gen.trip_config import Ui_tripConfig

import logging
logger = logging.getLogger(__name__)


class ConfigQtView(object):
    """
    """
    def __init__(self):
        self.ui = Ui_tripConfig()
        self.dialog = QtWidgets.QDialog()

        self.ui.setupUi(self.dialog)
        self._setup_callbacks()

    def show(self):
        self.dialog.show()
        self.dialog.exec_()

    def exit(self):
        self.dialog.close()

    def set_ok_callback(self, fun):
        self.ui.accept_buttonBox.accepted.connect(fun)

    def set_cancel_callback(self, fun):
        self.ui.accept_buttonBox.rejected.connect(fun)
