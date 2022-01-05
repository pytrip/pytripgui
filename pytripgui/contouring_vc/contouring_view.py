#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication, QDialog, QDialogButtonBox
from pytripgui.view.qt_gui import ContouringDialog


class ContouringView:
    def __init__(self, parent=None):
        self._ui: QDialog = ContouringDialog(parent)

        # set window text defaults
        self._initial_prompt = "Would you like to precalculate VOI contrours?"
        self._initial_warning = "This may take a few minutes, but it will speed up viewing the patient anatomy."
        self._before_calculation = "Getting ready..."
        self._progress_message = "Precalculating contours for VOI: \n{name} ({current}/{total})"
        self._calculation_warning = "This may take a few minutes..."
        self._finish_message = "Precalculating complete!"

    def _set_progress_label_text(self, text):
        self._ui.progress_label.setText(text)

    def _set_warning_label_text(self, text):
        self._ui.warning_label.setText(text)

    def _set_window_title(self, title):
        self._ui.setWindowTitle(title)

    def show(self):
        self._set_progress_label_text(self._initial_prompt)
        self._set_warning_label_text(self._initial_warning)
        self._ui.show()
        # we need to process events to let UI init take effect
        QApplication.processEvents()

    def _buttons_set_enabled(self, enabled):
        self._ui.button_box.setEnabled(enabled)

    def _set_buttons(self, flags):
        self._ui.button_box.setStandardButtons(flags)

    def update_accepted(self):
        self._set_progress_label_text(self._before_calculation)
        self._set_warning_label_text(self._calculation_warning)
        self._buttons_set_enabled(False)
        self._set_buttons(QDialogButtonBox.Ok)
        self._ui.button_box.button(QDialogButtonBox.Ok).clicked.connect(self._ui.accept)

    def update_progress(self, voi_name, current, total):
        self._set_progress_label_text(self._progress_message.format(name=voi_name, current=current+1, total=total))

    def update_finished(self):
        self._set_progress_label_text(self._finish_message)
        self._set_warning_label_text("")
        self._buttons_set_enabled(True)

    def connect_yes(self, callback):
        self._ui.button_box.button(QDialogButtonBox.Yes).clicked.connect(callback)
