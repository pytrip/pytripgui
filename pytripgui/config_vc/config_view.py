from pytripgui.view.qt_view_adapter import LineEdit, ComboBox
from pytripgui.view.qt_gui import UiTripConfig
from PyQt5.QtWidgets import QFileDialog

import logging
logger = logging.getLogger(__name__)


class ConfigQtView(object):
    stackedWidget_local_index = 0
    stackedWidget_remote_index = 1
    """
    """
    def __init__(self):
        self.ui = UiTripConfig()

        self.name = LineEdit(self.ui.configName_lineEdit)
        self.user_name = LineEdit(self.ui.username_lineEdit)
        self.password = LineEdit(self.ui.password_lineEdit)
        self.host_name = LineEdit(self.ui.host_lineEdit)

        self.configs = ComboBox(self.ui.configs_comboBox)

        self._setup_internal_callbacks()
        self.ui.local_radioButton.clicked.emit()

    def _setup_internal_callbacks(self):
        self.ui.wdirPath_pushButton.clicked.connect(self._browse_wdir)
        self.ui.tripPath_pushButton.clicked.connect(self._browse_trip_path)
        self.ui.hlut_pushButton.clicked.connect(self._browse_hlut_path)
        self.ui.dedx_pushButton.clicked.connect(self._browse_dedx_path)

        self.ui.local_radioButton.clicked.connect(self._on_local_radio_button_click)
        self.ui.remote_radioButton.clicked.connect(self._on_remote_radio_button_click)

    def _browse_wdir(self):
        selected_dir = QFileDialog.getExistingDirectory(
            self.ui,  "Select working directory", self.wdir_path,
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if selected_dir != "":
            self.wdir_path = selected_dir

    def _browse_trip_path(self):
        selected_dir = QFileDialog.getExistingDirectory(
            self.ui, "Select trip executable directory", self.trip_path,
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if selected_dir != "":
            self.trip_path = selected_dir

    def _browse_hlut_path(self):
        selected_file = QFileDialog.getOpenFileName(
            self.ui, "Select HLUT",  self.hlut_path, "Hounsfield lookup table (*.hlut)")
        if selected_file[0] != "":
            self.hlut_path = selected_file[0]

    def _browse_dedx_path(self):
        selected_file = QFileDialog.getOpenFileName(
            self.ui, "Select DEDX",  self.dedx_path, "Stopping power table (*.dedx)")
        if selected_file[0] != "":
            print(selected_file)
            self.dedx_path = selected_file[0]

    def _on_local_radio_button_click(self):
        self.ui.pathConfig_stackedWidget.setCurrentIndex(ConfigQtView.stackedWidget_local_index)

    def _on_remote_radio_button_click(self):
        self.ui.pathConfig_stackedWidget.setCurrentIndex(ConfigQtView.stackedWidget_remote_index)

    def show(self):
        self.ui.show()
        self.ui.exec_()

    def exit(self):
        self.ui.close()

    def set_ok_callback(self, fun):
        self.ui.accept_buttonBox.accepted.connect(fun)

    def set_cancel_callback(self, fun):
        self.ui.accept_buttonBox.rejected.connect(fun)

    @property
    def remote_execution(self):
        return self.ui.remote_radioButton.isChecked()

    @remote_execution.setter
    def remote_execution(self, remote_execution):
        if remote_execution:
            self.ui.remote_radioButton.setChecked(remote_execution)
            self.ui.remote_radioButton.clicked.emit()
        else:
            self.ui.local_radioButton.setChecked(remote_execution)
            self.ui.local_radioButton.clicked.emit()

    @property
    def wdir_path(self):
        return self.ui.wdirPath_lineEdit.text()

    @wdir_path.setter
    def wdir_path(self, wdir_path):
        self.ui.wdirPath_lineEdit.setText(wdir_path)

    @property
    def trip_path(self):
        return self.ui.tripPath_lineEdit.text()

    @trip_path.setter
    def trip_path(self, trip_path):
        self.ui.tripPath_lineEdit.setText(trip_path)

    @property
    def hlut_path(self):
        return self.ui.hlut_lineEdit.text()

    @hlut_path.setter
    def hlut_path(self, hlut_path):
        self.ui.hlut_lineEdit.setText(hlut_path)

    @property
    def dedx_path(self):
        return self.ui.dedx_lineEdit.text()

    @dedx_path.setter
    def dedx_path(self, dedx_path):
        self.ui.dedx_lineEdit.setText(dedx_path)
