from pytripgui.view.qt_gui import UiKernelDialog
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt
import os

import logging

logger = logging.getLogger(__name__)


class KernelQtView:
    """
    """
    def __init__(self):
        self.ui = UiKernelDialog()

        self._setup_internal_callbacks()
        self._disable_unimplemented()

    def _setup_internal_callbacks(self):
        self.ui.dddPath_pushButton.clicked.connect(self._browse_ddd_dir)
        self.ui.spcPath_pushButton.clicked.connect(self._browse_spc_dir)
        self.ui.sisPath_pushButton.clicked.connect(self._browse_sis_path)
        self.ui.kernelName_lineEdit.textChanged.connect(self._set_current_kernel_combobox_name)

    def _set_current_kernel_combobox_name(self, name):
        current_index = self.ui.beamKernel_comboBox.currentIndex()
        self.ui.beamKernel_comboBox.setItemText(current_index, name)

    def _browse_ddd_dir(self):
        selected_dir = QFileDialog.getExistingDirectory(self.ui, "Select DDD directory", self.ddd_dir_path,
                                                        QFileDialog.DontResolveSymlinks)
        if selected_dir != "":
            self.ddd_dir_path = os.path.join(selected_dir, "", "*")

    def _browse_spc_dir(self):
        selected_dir = QFileDialog.getExistingDirectory(self.ui, "Select SPC directory", self.spc_dir_path,
                                                        QFileDialog.DontResolveSymlinks)
        if selected_dir != "":
            self.spc_dir_path = os.path.join(selected_dir, "", "*")

    def _browse_sis_path(self):
        selected_file = QFileDialog.getOpenFileName(self.ui, "Select sis path", self.sis_path, "(*.sis)")
        if selected_file[0] != "":
            self.sis_path = selected_file[0]

    def _disable_unimplemented(self):
        self.ui.rippleFilter_checkBox.setDisabled(True)
        self.ui.importBeamKernel_pushButton.setDisabled(True)
        self.ui.exportBeamKernel_pushButton.setDisabled(True)

    def show(self):
        self.ui.show()
        self.ui.exec_()

    def exit(self):
        self.ui.close()

    def set_ok_callback(self, fun):
        self.ui.accept_buttonBox.accepted.connect(fun)

    def set_cancel_callback(self, fun):
        self.ui.accept_buttonBox.rejected.connect(fun)

    def set_selected_beam_kernel_callback(self, fun):
        self.ui.beamKernel_comboBox.currentIndexChanged.connect(fun)

    def new_beam_kernel_callback(self, fun):
        self.ui.newBeamKernel_pushButton.clicked.connect(fun)

    def remove_beam_kernel_callback(self, fun):
        self.ui.removeBeamKernel_pushButton.clicked.connect(fun)

    @property
    def ddd_dir_path(self):
        return self.ui.dddPath_lineEdit.text()

    @ddd_dir_path.getter
    def ddd_dir_path(self):
        return self.ui.dddPath_lineEdit.text()

    @ddd_dir_path.setter
    def ddd_dir_path(self, ddd_dir_path):
        self.ui.dddPath_lineEdit.setText(ddd_dir_path)

    @property
    def spc_dir_path(self):
        return self.ui.spcPath_lineEdit.text()

    @spc_dir_path.getter
    def spc_dir_path(self):
        return self.ui.spcPath_lineEdit.text()

    @spc_dir_path.setter
    def spc_dir_path(self, spc_dir_path):
        self.ui.spcPath_lineEdit.setText(spc_dir_path)

    @property
    def sis_path(self):
        return self.ui.sisPath_lineEdit.text()

    @sis_path.getter
    def sis_path(self):
        return self.ui.sisPath_lineEdit.text()

    @sis_path.setter
    def sis_path(self, spc_dir_path):
        self.ui.sisPath_lineEdit.setText(spc_dir_path)

    @property
    def comment(self):
        return self.ui.comment_lineEdit.text()

    @comment.getter
    def comment(self):
        return self.ui.comment_lineEdit.text()

    @comment.setter
    def comment(self, comment):
        self.ui.comment_lineEdit.setText(comment)

    @property
    def projectile_name(self):
        return self.ui.projectileName_lineEdit.text()

    @projectile_name.getter
    def projectile_name(self):
        return self.ui.projectileName_lineEdit.text()

    @projectile_name.setter
    def projectile_name(self, projectile_name):
        self.ui.projectileName_lineEdit.setText(projectile_name)

    @property
    def projectile_symbol(self):
        return self.ui.symbol_comboBox.currentData()

    @projectile_symbol.getter
    def projectile_symbol(self):
        return self.ui.symbol_comboBox.currentData()

    @projectile_symbol.setter
    def projectile_symbol(self, projectile_symbol):
        index_of_symbol = self.ui.symbol_comboBox.findData(projectile_symbol, Qt.UserRole)
        if index_of_symbol == -1:
            raise Exception("Given symbol wasn't found on the list")
        self.ui.symbol_comboBox.setCurrentIndex(index_of_symbol)

    @property
    def z(self):
        return self.ui.z_spinBox.value()

    @z.getter
    def z(self):
        return self.ui.z_spinBox.value()

    @z.setter
    def z(self, z):
        self.ui.z_spinBox.setValue(z)

    @property
    def a(self):
        return self.ui.a_spinBox.value()

    @a.getter
    def a(self):
        return self.ui.a_spinBox.value()

    @a.setter
    def a(self, a):
        self.ui.a_spinBox.setValue(a)

    @property
    def kernel_name(self):
        return self.ui.kernelName_lineEdit.text()

    @kernel_name.getter
    def kernel_name(self):
        return self.ui.kernelName_lineEdit.text()

    @kernel_name.setter
    def kernel_name(self, kernel_name):
        return self.ui.kernelName_lineEdit.setText(kernel_name)

    def add_kernel_with_name(self, kernel, kernel_name):
        self.ui.beamKernel_comboBox.addItem(kernel_name, kernel)

    def select_recently_added_kernel(self):
        kernel_index = self.ui.beamKernel_comboBox.count() - 1
        self.ui.beamKernel_comboBox.setCurrentIndex(kernel_index)

    def remove_current_kernel(self):
        kernel_index = self.ui.beamKernel_comboBox.currentIndex()
        self.ui.beamKernel_comboBox.removeItem(kernel_index)

    def get_all_kernels(self):
        kernels_count = self.ui.beamKernel_comboBox.count()
        kernels = []
        for i in range(kernels_count):
            kernel = self.ui.beamKernel_comboBox.itemData(i, Qt.UserRole)
            kernels.append(kernel)
        return kernels

    def replace_kernel_by_index(self, kernel, kernel_index):
        self.ui.beamKernel_comboBox.setItemData(kernel_index, kernel, Qt.UserRole)

    def setup_all_available_projectile_symbols(self, symbols):
        for symbol in symbols:
            self.ui.symbol_comboBox.addItem(symbol, symbol)

    def get_selected_kernel(self):
        return self.ui.beamKernel_comboBox.currentData(Qt.UserRole)
