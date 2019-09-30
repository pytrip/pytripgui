from pytripgui.view.qt_gui import UiMainWindow

from pytripgui.treewidget_vc.treewidget_view import TreeWidgetView

from PyQt5.QtWidgets import QFileDialog

import logging
logger = logging.getLogger(__name__)


class MainWindowQtView(object):
    def __init__(self):
        self.ui = UiMainWindow()

    def show(self):
        self.ui.show()

    def exit(self):
        self.ui.close()

    def get_patient_tree_view(self):
        return TreeWidgetView(self.ui.patient_treeWidget)

    def browse_file_path(self, name, extension, path=None):
        """
        :return full file path, or empty string
        """
        selected_file = QFileDialog.getOpenFileName(
            self.ui,
            name,
            path,
            extension)
        return selected_file[0]

    def show_info(self, name, content):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self.ui, name, content)

    @property
    def open_voxelplan_callback(self):
        return None

    @open_voxelplan_callback.setter
    def open_voxelplan_callback(self, callback):
        self.ui.actionOpen_Voxelplan.triggered.connect(callback)
