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
        self.set_model_from_view()
        self.user_clicked_save = True
        self.view.exit()

    def _exit(self):
        self.view.exit()

    def set_view_from_model(self):
        self.view.wdir_path = self.model.wdir_path
        self.view.trip_path = self.model.trip_path
        self.view.hlut_path = self.model.hlut_path
        self.view.dedx_path = self.model.dedx_path

    def set_model_from_view(self):
        self.model.wdir_path = self.view.wdir_path
        self.model.trip_path = self.view.trip_path
        self.model.hlut_path = self.view.hlut_path
        self.model.dedx_path = self.view.dedx_path
