import logging
logger = logging.getLogger(__name__)


class ConfigController(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.user_clicked_save = False

    def set_view_from_model(self):
        model = self.model
        view = self.view

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

    def set_model_from_view(self):
        model = self.model
        view = self.view
