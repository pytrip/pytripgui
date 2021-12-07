

#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget

from pytripgui.view.qt_gui import LoadingFileDialog


class LoadingFileView:
    def __init__(self, parent=None):
        self._ui: QWidget = LoadingFileDialog(parent)
        self._ui.info_label.setText('dupa')

    def set_info_label_text(self, text):
        self._ui.info_label.setText(text)

    def show(self):
        self._ui.show()
        self._ui.exec_()


class LoadingFileController:
    def __init__(self):
        self._view = LoadingFileView()
