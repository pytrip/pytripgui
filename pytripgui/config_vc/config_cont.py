import logging
logger = logging.getLogger(__name__)


class ConfigController(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.user_clicked_save = False
        self._setup_ok_and_cancel_buttons_callbacks()

    def _setup_ok_and_cancel_buttons_callbacks(self):
        self.view.set_ok_callback(self._save_and_exit)
        self.view.set_cancel_callback(self._exit)

    def _save_and_exit(self):
        self.set_model_from_view(self.model[0])
        self.user_clicked_save = True
        self.view.exit()

    def _exit(self):
        self.view.exit()

    def set_view_from_model(self):
        if not self.model:
            return

        self.view.configs.fill(self.model, lambda item: item.name)
        self.view.configs.emit_on_item_change(self._on_item_change_callback)

        self.set_current_config(self.model[0])

    def _on_item_change_callback(self, current_index):
        print(current_index)
        # lambda current_index: self.set_current_config(self.model[current_index])

    def set_current_config(self, config):
        self.view.remote_execution = config.remote_execution
        self.view.name.text = config.name
        self.view.wdir_path = config.wdir_path
        self.view.trip_path = config.trip_path
        self.view.hlut_path = config.hlut_path
        self.view.dedx_path = config.dedx_path
        self.view.host_name.text = config.host_name
        self.view.user_name.text = config.user_name
        self.view.password.text = config.password

    def set_model_from_view(self, config):
        config.remote_execution = self.view.remote_execution
        config.name = self.view.name.text
        config.wdir_path = self.view.wdir_path
        config.trip_path = self.view.trip_path
        config.hlut_path = self.view.hlut_path
        config.dedx_path = self.view.dedx_path
        config.host_name = self.view.host_name.text
        config.user_name = self.view.user_name.text
        config.password = self.view.password.text
