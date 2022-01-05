#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication, QDialog
from pytripgui.view.qt_gui import LoadingFileDialog


class LoadingFileView:
    def __init__(self, parent=None, window_title=None,
                 progress_message=None, finish_message=None):
        # define default text strings
        if not window_title:
            window_title = "Loading..."
        if not progress_message:
            progress_message = "Loading, please wait..."
        if not finish_message:
            finish_message = "Loading complete."

        self._ui: QDialog = LoadingFileDialog(parent)

        # set window text
        self.set_window_title(window_title)
        self.set_info_label_text(progress_message)
        self._finish_message = finish_message

    def set_info_label_text(self, text):
        self._ui.info_label.setText(text)

    def set_window_title(self, title):
        self._ui.setWindowTitle(title)

    def show(self):
        self._ui.show()
        # we need to process events to let UI init take effect
        QApplication.processEvents()

    def _ok_button_set_enabled(self, enabled):
        self._ui.ok_button.setEnabled(enabled)

    def update_finished(self):
        self.set_info_label_text(self._finish_message)
        self._ok_button_set_enabled(True)

    def connect_finished(self, callback):
        self._ui.finished.connect(callback)

    def reject(self):
        self._ui.reject()
