from pytripgui.view.qt_gui import UiExecuteDialog


class ExecutorQtView(object):
    def __init__(self, parent=None):
        self._ui = UiExecuteDialog(parent)
        self._setup_internal_callbacks()

    def show(self):
        self._ui.show()
        self._ui.exec_()

    def exit(self):
        self._ui.close()

    def set_ok_callback(self, fun):
        self._ui.accept_ButtonBox.accepted.connect(fun)

    def set_cancel_callback(self, fun):
        self._ui.accept_ButtonBox.rejected.connect(fun)

    def _setup_internal_callbacks(self):
        pass

    def append_log(self, text):
        self._ui.stdout_textBrowser.append(text)
