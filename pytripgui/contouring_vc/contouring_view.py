#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication, QDialog, QDialogButtonBox
from pytripgui.view.qt_gui import LoadingFileDialog


class ContouringView:
    def __init__(self, parent=None, window_title=None,
                 progress_message=None, warning_message=None, finish_message=None):
        # define default text strings
        if not progress_message:
            progress_message = "Loading, please wait..."
        if not finish_message:
            finish_message = "Loading complete."

        self._ui: QDialog = LoadingFileDialog(parent)

        # set window text
        if window_title:
            self.set_window_title(window_title)
        if progress_message:
            self.set_info_label_text(progress_message)
        if warning_message:
            self._warning_message = warning_message
        if finish_message:
            self._finish_message = finish_message

    def set_progress_label_text(self, text):
        self._ui.progress_label.setText(text)

    def set_warning_label_text(self, text):
        self._ui.warning_label.setText(text)

    def set_window_title(self, title):
        self._ui.setWindowTitle(title)

    def show(self):
        self._ui.show()
        # we need to process events to let UI init take effect
        QApplication.processEvents()

    def _buttons_set_enabled(self, enabled):
        self._ui.button_box.setEnabled(enabled)

    def _change_buttons(self, flags):
        self._ui.button_box.standardButtons

    def update_finished(self):
        self.set_info_label_text(self._finish_message)
        self._buttons_set_enabled(True)

    def connect_yes(self, callback):
        self._ui.button_box.button(QDialogButtonBox.Yes).clicked.connect(callback)

    def reject(self):
        self._ui.reject()
