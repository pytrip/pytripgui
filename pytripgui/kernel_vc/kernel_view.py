from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from pytripgui.view.gen.kernel import Ui_KernelDialog

import logging
logger = logging.getLogger(__name__)


class KernelQtView(object):
    """
    """
    def __init__(self):
        self.ui = Ui_KernelDialog()
        self.dialog = QtWidgets.QDialog()

        self.ui.setupUi(self.dialog)
        # self._setup_internal_callbacks()
        # self._disable_unimplemented()

    def _setup_internal_callbacks(self):
        self.ui.wdirPath_pushButton.clicked.connect(self._browse_wdir)
        self.ui.tripPath_pushButton.clicked.connect(self._browse_trip_path)
        self.ui.hlut_pushButton.clicked.connect(self._browse_hlut_path)
        self.ui.dedx_pushButton.clicked.connect(self._browse_dedx_path)

    def _browse_wdir(self):
        selected_dir = QFileDialog.getExistingDirectory(
            self.dialog,
            "Select working directory",
            self.wdir_path,
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if selected_dir != "":
            self.wdir_path = selected_dir

    def _browse_trip_path(self):
        selected_dir = QFileDialog.getExistingDirectory(
            self.dialog,
            "Select trip executable directory",
            self.trip_path,
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if selected_dir != "":
            self.trip_path = selected_dir

    def show(self):
        self.dialog.show()
        self.dialog.exec_()

    def exit(self):
        self.dialog.close()

    def set_ok_callback(self, fun):
        self.ui.accept_buttonBox.accepted.connect(fun)

    def set_cancel_callback(self, fun):
        self.ui.accept_buttonBox.rejected.connect(fun)

    @property
    def wdir_path(self):
        return self.ui.wdirPath_lineEdit.text()

    @wdir_path.getter
    def wdir_path(self):
        return self.ui.wdirPath_lineEdit.text()

    @wdir_path.setter
    def wdir_path(self, wdir_path):
        self.ui.wdirPath_lineEdit.setText(wdir_path)

    def add_kernel_with_name(self, kernel, kernel_name):
        self.ui.beamKernel_comboBox.addItem(kernel_name, kernel)
