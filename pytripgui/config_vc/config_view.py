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
        self._ui = UiTripConfig()

        self.name = LineEdit(self._ui.configName_lineEdit)
        self.user_name = LineEdit(self._ui.username_lineEdit)
        self.password = LineEdit(self._ui.password_lineEdit)
        self.host_name = LineEdit(self._ui.host_lineEdit)

        self.configs = ComboBox(self._ui.configs_comboBox)

        self._setup_internal_callbacks()
        self._ui.local_radioButton.clicked.emit()

    def _setup_internal_callbacks(self):
        self._ui.wdirPath_pushButton.clicked.connect(self._browse_wdir)
        self._ui.tripPath_pushButton.clicked.connect(self._browse_trip_path)
        self._ui.hlut_pushButton.clicked.connect(self._browse_hlut_path)
        self._ui.dedx_pushButton.clicked.connect(self._browse_dedx_path)

        self._ui.local_radioButton.clicked.connect(self._on_local_radio_button_click)
        self._ui.remote_radioButton.clicked.connect(self._on_remote_radio_button_click)

    def _browse_wdir(self):
        selected_dir = QFileDialog.getExistingDirectory(
            self._ui,  "Select working directory", self.wdir_path,
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if selected_dir != "":
            self.wdir_path = selected_dir

    def _browse_trip_path(self):
        selected_dir = QFileDialog.getExistingDirectory(
            self._ui, "Select trip executable directory", self.trip_path,
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if selected_dir != "":
            self.trip_path = selected_dir

    def _browse_hlut_path(self):
        selected_file = QFileDialog.getOpenFileName(
            self._ui, "Select HLUT",  self.hlut_path, "Hounsfield lookup table (*.hlut)")
        if selected_file[0] != "":
            self.hlut_path = selected_file[0]

    def _browse_dedx_path(self):
        selected_file = QFileDialog.getOpenFileName(
            self._ui, "Select DEDX",  self.dedx_path, "Stopping power table (*.dedx)")
        if selected_file[0] != "":
            print(selected_file)
            self.dedx_path = selected_file[0]

    def _on_local_radio_button_click(self):
        self._ui.pathConfig_stackedWidget.setCurrentIndex(ConfigQtView.stackedWidget_local_index)

    def _on_remote_radio_button_click(self):
        self._ui.pathConfig_stackedWidget.setCurrentIndex(ConfigQtView.stackedWidget_remote_index)

    def show(self):
        self._ui.show()
        self._ui.exec_()

    def exit(self):
        self._ui.close()

    def set_ok_callback(self, fun):
        self._ui.accept_buttonBox.accepted.connect(fun)

    def set_cancel_callback(self, fun):
        self._ui.accept_buttonBox.rejected.connect(fun)

    @property
    def remote_execution(self):
        return self._ui.remote_radioButton.isChecked()

    @remote_execution.setter
    def remote_execution(self, remote_execution):
        if remote_execution:
            self._ui.remote_radioButton.setChecked(True)
            self._ui.remote_radioButton.clicked.emit()
        else:
            self._ui.local_radioButton.setChecked(True)
            self._ui.local_radioButton.clicked.emit()

    @property
    def wdir_path(self):
        return self._ui.wdirPath_lineEdit.text()

    @wdir_path.setter
    def wdir_path(self, wdir_path):
        self._ui.wdirPath_lineEdit.setText(wdir_path)

    @property
    def trip_path(self):
        return self._ui.tripPath_lineEdit.text()

    @trip_path.setter
    def trip_path(self, trip_path):
        self._ui.tripPath_lineEdit.setText(trip_path)

    @property
    def hlut_path(self):
        return self._ui.hlut_lineEdit.text()

    @hlut_path.setter
    def hlut_path(self, hlut_path):
        self._ui.hlut_lineEdit.setText(hlut_path)

    @property
    def dedx_path(self):
        return self._ui.dedx_lineEdit.text()

    @dedx_path.setter
    def dedx_path(self, dedx_path):
        self._ui.dedx_lineEdit.setText(dedx_path)
