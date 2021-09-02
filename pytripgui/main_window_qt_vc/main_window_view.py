import logging

from PyQt5.QtWidgets import QFileDialog

from pytripgui.view.qt_gui import UiMainWindow
from pytripgui.config_vc import ConfigQtView
from pytripgui.kernel_vc import KernelQtView

logger = logging.getLogger(__name__)


class MainWindowQtView:
    def __init__(self):
        self.ui = UiMainWindow()

    def show(self):
        self.ui.show()

    def exit(self):
        self.ui.close()

    def add_widget(self, widget):
        self.ui.main_layout.addWidget(widget)

    @staticmethod
    def get_trip_config_view():
        return ConfigQtView()

    @staticmethod
    def get_kernel_config_view():
        return KernelQtView()

    def browse_file_path(self, name, extension, path=None):
        """
        Browse for an existing file.

        :return full file path (absolute), or empty string if browsing was aborted
        """
        selected_file_path, selected_file_extension = QFileDialog.getOpenFileName(self.ui, name, path, extension)
        return selected_file_path

    def save_file_path(self, caption, extension, path=None):
        """
        Select the name and directory of a file to be created.

        :return full file path (absolute), or empty string if browsing was aborted
        """
        selected_file_path, selected_file_extension = QFileDialog.getSaveFileName(self.ui, caption, path, extension)
        return selected_file_path

    def browse_folder_path(self, name, path=None):
        """
        Browse for an existing directory.

        :return full directory path (absolute), or empty string if browsing was aborted
        """
        dialog = QFileDialog(self.ui, name, path)
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setOptions(QFileDialog.ShowDirsOnly)
        dialog.exec_()

        # only one directory can be selected in dialog window,
        # but the selectedFiles method only returns a list, so [0] is selected
        selected_path = dialog.selectedFiles()[0]

        if dialog.result() == QFileDialog.Accepted:
            return selected_path
        return ""

    def show_info(self, name, content):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self.ui, name, content)

    @property
    def open_voxelplan_callback(self):
        return None

    @open_voxelplan_callback.setter
    def open_voxelplan_callback(self, callback):
        self.ui.actionOpen_Voxelplan.triggered.connect(callback)

    @property
    def open_dicom_callback(self):
        return None

    @open_dicom_callback.setter
    def open_dicom_callback(self, callback):
        self.ui.actionOpen_Dicom.triggered.connect(callback)

    @property
    def open_kernels_configurator_callback(self):
        return None

    @open_kernels_configurator_callback.setter
    def open_kernels_configurator_callback(self, callback):
        self.ui.actionBeam_Kernels.triggered.connect(callback)

    @property
    def add_new_plan_callback(self):
        return None

    @add_new_plan_callback.setter
    def add_new_plan_callback(self, callback):
        self.ui.actionNew_Plan.triggered.connect(callback)

    @property
    def about_callback(self):
        return None

    @about_callback.setter
    def about_callback(self, callback):
        self.ui.actionAbout.triggered.connect(callback)

    @property
    def trip_config_callback(self):
        return None

    @trip_config_callback.setter
    def trip_config_callback(self, callback):
        self.ui.actionTRiP98_Config.triggered.connect(callback)

    @property
    def exit_callback(self):
        return None

    @exit_callback.setter
    def exit_callback(self, callback):
        self.ui.actionExit.triggered.connect(callback)

    @property
    def action_add_patient(self):
        return None

    @action_add_patient.setter
    def action_add_patient(self, callback):
        self.ui.actionAdd_Patient.triggered.connect(callback)

    @property
    def action_create_field(self):
        return None

    @action_create_field.setter
    def action_create_field(self, callback):
        self.ui.actionCreate_field.triggered.connect(callback)

    @property
    def action_execute_plan(self):
        return None

    @action_execute_plan.setter
    def action_execute_plan(self, callback):
        self.ui.actionExecute_Plan.triggered.connect(callback)

    def action_create_field_set_enable(self, enabled):
        self.ui.actionCreate_field.setEnabled(enabled)

    def action_create_plan_set_enable(self, enabled):
        self.ui.actionNew_Plan.setEnabled(enabled)

    def action_execute_plan_set_enable(self, enabled):
        self.ui.actionExecute_Plan.setEnabled(enabled)

    @property
    def action_open_tree(self):
        return None

    @action_open_tree.setter
    def action_open_tree(self, callback):
        self.ui.actionTree.triggered.connect(callback)
        self.ui.actionTree.setCheckable(True)
        self.ui.actionTree.setChecked(True)

    @property
    def action_open_tree_checked(self):
        return self.ui.actionTree.isChecked()
