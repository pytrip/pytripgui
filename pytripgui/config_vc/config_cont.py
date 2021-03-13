from pytripgui.plan_executor.trip_config import Trip98ConfigModel

from copy import deepcopy
import logging
logger = logging.getLogger(__name__)


class ConfigController(object):
    def __init__(self, model, view):
        self.model = deepcopy(model)
        self.view = view
        self.user_clicked_save = False
        self._setup_ok_and_cancel_buttons_callbacks()

        if not self.model:
            self.model = [Trip98ConfigModel()]

    def _setup_ok_and_cancel_buttons_callbacks(self):
        self.view.set_ok_callback(self._save_and_exit)
        self.view.set_cancel_callback(self._exit)

        self.view.name.emit_on_text_change(
            lambda text: self.view.configs.set_current_item_text(text))

    def _save_and_exit(self):
        self.user_clicked_save = True
        self._exit()

    def _exit(self):
        if self.view.configs.count:
            self._set_model_from_view(
                self.model[self.view.configs.current_index])
        self.view.exit()

    def set_view_from_model(self):
        if not self.model:
            return

        self.view.configs.fill(self.model, lambda item: item.name)
        self.view.configs.emit_on_item_change(self._on_item_change_callback)

        self._set_current_config(self.model[0])

    def _on_item_change_callback(self):
        self._set_model_from_view(self.model[self.view.configs.last_index])
        self._set_current_config(self.model[self.view.configs.current_index])

    def _set_current_config(self, config):
        self.view.remote_execution = config.remote_execution
        self.view.name.text = config.name
        self.view.wdir_path.text = config.wdir_path
        self.view.trip_path.text = config.trip_path
        self.view.hlut_path.text = config.hlut_path
        self.view.dedx_path.text = config.dedx_path
        self.view.host_name.text = config.host_name
        self.view.user_name.text = config.user_name
        self.view.password.text = config.password
        self.view.wdir_remote_path.text = config.wdir_remote_path

    def _set_model_from_view(self, config):
        config.remote_execution = self.view.remote_execution
        config.name = self.view.name.text
        config.wdir_path = self.view.wdir_path.text
        config.trip_path = self.view.trip_path.text
        config.hlut_path = self.view.hlut_path.text
        config.dedx_path = self.view.dedx_path.text
        config.host_name = self.view.host_name.text
        config.user_name = self.view.user_name.text
        config.password = self.view.password.text
        config.wdir_remote_path = self.view.wdir_remote_path.text
