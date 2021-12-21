

#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication, QDialog
from pytripgui.view.qt_gui import LoadingFileDialog


class LoadingFileView:

    def __init__(self, file_path, load_function, parent=None, window_title=None,
                 progress_message=None, finish_message=None):
        if not window_title:
            window_title = "Loading..."
        if not progress_message:
            progress_message = "Loading, please wait..."
        if not finish_message:
            finish_message = "Loading complete."

        self._ui: QDialog = LoadingFileDialog(parent)
        self.file_path = file_path
        self.load_function = load_function

        self.set_window_title(window_title)
        self.set_info_label_text(progress_message)
        self.finish_message = finish_message

        # self._thread = LoadingFileThread(file_path, app_controller, self.on_thread_terminate_2)
        # self._thread.done.connect(self.on_thread_terminate)

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
        # self._thread.start()
        loaded = self.load_function(self.file_path)
        # self.list_parent, self.new_item = self.app_controller.open_voxelplan(self.file_path)
        # self.app_controller.model.patient_tree.add_new_item(parent_item=patient_list_parent, item=new_patient)
        # self.done.emit()
        if loaded:
            self._update_finished()
        else:
            self._ui.destroy()

    # @pyqtSlot(name="on_thread_terminate")
    # def on_thread_terminate(self):
    #     self.set_info_label_text('Complete!')
    #     print(self._thread.new_item)
    #     print(self._thread.list_parent)
    #     self._ui.ok_button.setEnabled(True)

    def _update_finished(self):
        self.set_info_label_text(self.finish_message)
        # print(new_item)
        # print(list_parent)

        # self._app_controller.add_new_item(list_parent, new_item)
        self._ui.ok_button.setEnabled(True)


class LoadingFileController:
    def __init__(self):
        self._view = LoadingFileView()
