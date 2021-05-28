from pytripgui.view.qt_view_adapter import LineEdit, ComboBox, UserInfoBox, PushButton
from pytripgui.view.qt_gui import UiTripConfig
from PyQt5.QtWidgets import QFileDialog

import logging

logger = logging.getLogger(__name__)


class ConfigQtView:
    stackedWidget_local_index = 0
    stackedWidget_remote_index = 1
    """
    """
    def __init__(self):
        self._ui = UiTripConfig()

        self.name = LineEdit(self._ui.configName_lineEdit)
        self.user_name = LineEdit(self._ui.username_lineEdit)
        self.pkey_path = LineEdit(self._ui.pkey_lineEdit)
        self.password = LineEdit(self._ui.password_lineEdit)
        self.host_name = LineEdit(self._ui.host_lineEdit)
        self.dedx_path = LineEdit(self._ui.dedx_lineEdit)
        self.hlut_path = LineEdit(self._ui.hlut_lineEdit)
        self.wdir_path = LineEdit(self._ui.wdirPath_lineEdit)
        self.trip_path = LineEdit(self._ui.tripPath_lineEdit)

        self.add_button = PushButton(self._ui.add_pushButton)
        self.remove_button = PushButton(self._ui.remove_pushButton)

        self.wdir_remote_path = LineEdit(self._ui.wdirRemote_lineEdit)

        self.configs = ComboBox(self._ui.configs_comboBox)

        self.info_box = UserInfoBox(self._ui)

        self._setup_internal_callbacks()
        self._ui.local_radioButton.clicked.emit()

        self.name.emit_on_text_change(self.configs.set_current_item_text)

    def test_ssh_clicked_callback_connect(self, callback):
        self._ui.testSsh_pushButton.clicked.connect(callback)

    def _setup_internal_callbacks(self):
        self._ui.wdirPath_pushButton.clicked.connect(self._browse_wdir)
        self._ui.tripPath_pushButton.clicked.connect(self._browse_trip_path)
        self._ui.hlut_pushButton.clicked.connect(self._browse_hlut_path)
        self._ui.dedx_pushButton.clicked.connect(self._browse_dedx_path)
        self._ui.pKey_pushButton.clicked.connect(self._browse_pkey_path)

        self._ui.local_radioButton.clicked.connect(self._on_local_radio_button_click)
        self._ui.remote_radioButton.clicked.connect(self._on_remote_radio_button_click)

    def _browse_wdir(self):
        selected_dir = QFileDialog.getExistingDirectory(self._ui, "Select working directory", self.wdir_path.text,
                                                        QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if selected_dir != "":
            self.wdir_path.text = selected_dir

    def _browse_trip_path(self):
        selected_dir = QFileDialog.getExistingDirectory(self._ui, "Select trip executable directory",
                                                        self.trip_path.text,
                                                        QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if selected_dir != "":
            self.trip_path.text = selected_dir

    def _browse_hlut_path(self):
        selected_file = QFileDialog.getOpenFileName(self._ui, "Select HLUT", self.hlut_path.text,
                                                    "Hounsfield lookup table (*.hlut)")
        if selected_file[0] != "":
            self.hlut_path.text = selected_file[0]

    def _browse_dedx_path(self):
        selected_file = QFileDialog.getOpenFileName(self._ui, "Select DEDX", self.dedx_path.text,
                                                    "Stopping power table (*.dedx)")
        if selected_file[0] != "":
            print(selected_file)
            self.dedx_path.text = selected_file[0]

    def _browse_pkey_path(self):
        selected_file = QFileDialog.getOpenFileName(self._ui, "Select private key for SSH connection",
                                                    self.pkey_path.text, "Private key (*)")
        if selected_file[0] != "":
            self.pkey_path.text = selected_file[0]

    def _on_local_radio_button_click(self):
        self._ui.local_radioButton.setChecked(True)
        self._ui.tripPath_pushButton.setVisible(True)
        self._ui.hlut_pushButton.setVisible(True)
        self._ui.dedx_pushButton.setVisible(True)
        self._ui.ssh_GroupBox.setEnabled(False)
        self._ui.remoteLocal_groupBox.setTitle("Local paths")

    def _on_remote_radio_button_click(self):
        self._ui.remote_radioButton.setChecked(True)
        self._ui.tripPath_pushButton.setVisible(False)
        self._ui.hlut_pushButton.setVisible(False)
        self._ui.dedx_pushButton.setVisible(False)
        self._ui.ssh_GroupBox.setEnabled(True)
        self._ui.remoteLocal_groupBox.setTitle("Remote paths")

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
            self._ui.remote_radioButton.clicked.emit()
        else:
            self._ui.local_radioButton.clicked.emit()
