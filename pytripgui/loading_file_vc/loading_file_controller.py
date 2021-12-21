#!/usr/bin/python
# -*- coding: utf-8 -*-
from pytripgui.loading_file_vc.loading_file_view import LoadingFileView


class LoadingFileController:
    # TODO split VC responsibility
    def __init__(self, file_path, load_function, parent=None, window_title=None,
                 progress_message=None, finish_message=None):
        self._view = LoadingFileView(parent=parent, window_title=window_title,
                                     progress_message=progress_message, finish_message=finish_message)
        self._file_path = file_path
        self._load_function = load_function

    def start(self):
        self._view.show()
        # execute the loading function (e.g. opening DICOM)
        loaded = self._load_function(self._file_path)
        if loaded:
            self._update_finished()
        else:
            # if the user canceled opening, instantly close the loading window without waiting for confirmation
            self._view.reject()

    def _update_finished(self):
        self._view.update_finished()
