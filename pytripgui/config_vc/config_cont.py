from pytripgui.plan_executor.trip_config import Trip98ConfigModel
from paramiko import ssh_exception

import logging

logger = logging.getLogger(__name__)


class ConfigController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.user_clicked_save = False
        self._setup_callbacks()

        self.view.test_ssh_clicked_callback_connect(self._test_ssh)

        if not self.model:
            self.model = [Trip98ConfigModel()]

    def _setup_callbacks(self):
        self.view.set_ok_callback(self._save_and_exit)
        self.view.set_cancel_callback(self._exit)

        self.view.add_button.emit_on_click(lambda: self.view.configs.append_element(Trip98ConfigModel(), ""))
        self.view.remove_button.emit_on_click(self.view.configs.remove_current_item)

    def _save_and_exit(self):
        self.user_clicked_save = True
        self.model = self.view.configs.data
        self._exit()

    def _exit(self):
        if self.view.configs.count:
            self._set_model_from_view()
        self.view.exit()

    def set_view_from_model(self):
        self.view.configs.fill(self.model, lambda item: item.name)
        self.view.configs.emit_on_item_change(self._on_item_change_callback)
        self._set_current_config()

    def _on_item_change_callback(self):
        self._set_model_from_view()
        self._set_current_config()

    def _set_current_config(self):
        config = self.view.configs.current_data

        self.view.remote_execution = config.remote_execution
        self.view.name.text = config.name
        self.view.wdir_path.text = config.wdir_path
        self.view.trip_path.text = config.trip_path
        self.view.hlut_path.text = config.hlut_path
        self.view.dedx_path.text = config.dedx_path
        self.view.host_name.text = config.host_name
        self.view.user_name.text = config.user_name
        self.view.pkey_path.text = config.pkey_path
        self.view.password.text = config.password
        self.view.wdir_remote_path.text = config.wdir_remote_path

    def _set_model_from_view(self):
        config = self.view.configs.last_data

        # after you delete config, there is nothing in last_data
        if not config:
            return

        config.remote_execution = self.view.remote_execution
        config.name = self.view.name.text
        config.wdir_path = self.view.wdir_path.text
        config.trip_path = self.view.trip_path.text
        config.hlut_path = self.view.hlut_path.text
        config.dedx_path = self.view.dedx_path.text
        config.host_name = self.view.host_name.text
        config.user_name = self.view.user_name.text
        config.pkey_path = self.view.pkey_path.text
        config.password = self.view.password.text
        config.wdir_remote_path = self.view.wdir_remote_path.text

    def _test_ssh(self):
        import paramiko
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        key_path = None
        if self.view.pkey_path.text:
            key_path = self.view.pkey_path.text

        try:
            ssh.connect(hostname=self.view.host_name.text,
                        username=self.view.user_name.text,
                        password=self.view.password.text,
                        key_filename=key_path)
        except ssh_exception.AuthenticationException as e:
            self.view.info_box.show_error("Authentication", e.__str__())
        except FileNotFoundError as e:
            self.view.info_box.show_error("File not found", e.__str__())
        except ValueError as e:
            self.view.info_box.show_error("Value", e.__str__())
        else:

            sftp = ssh.open_sftp()
            try:
                sftp.stat(self.view.wdir_remote_path.text)
            except FileNotFoundError:
                self.view.info_box.show_error("File not found", "Remote working directory doesn't exist")
            else:
                self.view.info_box.show_info("SSH Connection", "Everything OK")

        ssh.close()
