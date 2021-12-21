from threading import Thread

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication


class LoadingFileThread(QThread):
    done = pyqtSignal()

    def __init__(self, file_path, app_controller, terminate_callback):
        super().__init__()
        self.file_path = file_path
        self._app_controller = app_controller
        self.list_parent = None
        self.new_item = None
        self.terminate_callback = terminate_callback

    def run(self):
        print("thread started")
        # QApplication.processEvents()
        self.list_parent, self.new_item = self._app_controller.open_voxelplan(self.file_path)
        # self.list_parent, self.new_item = self.app_controller.open_voxelplan(self.file_path)
        # QApplication.processEvents()
        # self.app_controller.model.patient_tree.add_new_item(parent_item=patient_list_parent, item=new_patient)
        print("open_voxelplan finished")
        print("finished")
        # self.done.emit()
        self.terminate_callback(self.list_parent, self.new_item)

