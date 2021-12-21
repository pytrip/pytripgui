#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication, QDialog
from pytripgui.view.qt_gui import LoadingFileDialog


class LoadingFileView:
    def __init__(self, file_path, load_function, parent=None, window_title=None,
                 progress_message=None, finish_message=None):
        # default text strings
        if not window_title:
            window_title = "Loading..."
        if not progress_message:
            progress_message = "Loading, please wait..."
        if not finish_message:
            finish_message = "Loading complete."

        self._ui: QDialog = LoadingFileDialog(parent)
        self.file_path = file_path
        self.load_function = load_function

        # setting window text
        self.set_window_title(window_title)
        self.set_info_label_text(progress_message)
        self.finish_message = finish_message

    def set_info_label_text(self, text):
        self._ui.info_label.setText(text)

    def set_window_title(self, title):
        self._ui.setWindowTitle(title)

    def show(self):
        self._ui.show()
        # we need to process events to let UI init take effect
        QApplication.processEvents()
        self.start()

    def start(self):
        # execute the loading function (e.g. opening DICOM)
        loaded = self.load_function(self.file_path)
        if loaded:
            self._update_finished()
        else:
            # if the user canceled opening, instantly close the loading window without waiting for confirmation
            self._ui.destroy()

    def _update_finished(self):
        self.set_info_label_text(self.finish_message)
        self._ui.ok_button.setEnabled(True)


class LoadingFileController:
    # TODO split VC responsibility
    def __init__(self):
        self._view = LoadingFileView()
