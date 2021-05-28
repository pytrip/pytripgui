from pytripgui.view.qt_gui import UiExecuteDialog


class ExecutorQtView:
    def __init__(self, parent=None):
        self._ui = UiExecuteDialog(parent)
        self._setup_internal_callbacks()

    def show(self):
        self._ui.show()
        self._ui.exec_()

    def _exit(self):
        self._ui.close()

    def _set_ok_callback(self, fun):
        self._ui.accept_ButtonBox.accepted.connect(fun)

    def _setup_internal_callbacks(self):
        self._set_ok_callback(self._exit)

    def append_log(self, text):
        self._ui.stdout_textBrowser.append(text)

    def enable_ok_button(self):
        self._ui.accept_ButtonBox.setEnabled(True)
