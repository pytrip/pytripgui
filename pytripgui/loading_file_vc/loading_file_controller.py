#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from typing import Callable, Tuple

from pytripgui.loading_file_vc.loading_file_view import LoadingFileView

logger = logging.getLogger(__name__)


class LoadingFileController:
    def __init__(self, load_function: Callable, function_args: Tuple, parent=None, window_title=None,
                 progress_message=None, finish_message=None):
        self._view = LoadingFileView(parent=parent, window_title=window_title,
                                     progress_message=progress_message, finish_message=finish_message)
        self._args = function_args
        self._load_function = load_function

    def start(self):
        self._view.show()
        # execute the loading function (e.g. opening DICOM)
        loaded = self._load_function(*self._args)
        if loaded:
            self._update_finished()
        else:
            # if the user canceled opening, instantly close the loading window without waiting for confirmation
            self._view.reject()

    def connect_finished(self, callback):
        self._view.connect_finished(callback)

    def _update_finished(self):
        self._view.update_finished()
