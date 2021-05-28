from pytripgui.view.qt_gui import UiExecuteConfigDialog
from pytripgui.view.qt_view_adapter import ComboBox


class ExecuteConfigView:
    def __init__(self, model, ui):
        self._ui = UiExecuteConfigDialog(ui)
        self.config = None

        self._configs = ComboBox(self._ui.configs_comboBox)
        self._configs.fill(model, lambda config: config.name)
        self._setup_ok_and_cancel_buttons_callbacks()

    def _setup_ok_and_cancel_buttons_callbacks(self):
        self.set_ok_callback(self._execute)
        self.set_cancel_callback(self._exit)

    def set_ok_callback(self, fun):
        self._ui.accept_buttonBox.accepted.connect(fun)

    def set_cancel_callback(self, fun):
        self._ui.accept_buttonBox.rejected.connect(fun)

    def _execute(self):
        self.config = self._configs.current_data
        self._exit()

    def _exit(self):
        self._ui.close()

    def show(self):
        self._ui.show()
        self._ui.exec_()
