import logging

from PyQt5.QtWidgets import QFileDialog

from pytripgui.view.qt_gui import UiMainWindow
from pytripgui.config_vc import ConfigQtView
from pytripgui.kernel_vc import KernelQtView
from pytripgui.treewidget_vc.treewidget_view import TreeWidgetView
from pytripgui.viewcanvas_vc.viewcanvas_view import ViewCanvasView

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

    def get_viewcanvas_view(self):
        one_viewcanvas = ViewCanvasView()
        self.ui.tab_Vlayout.addWidget(one_viewcanvas.widget())
        return one_viewcanvas

    @staticmethod
    def get_trip_config_view():
        return ConfigQtView()

    @staticmethod
    def get_kernel_config_view():
        return KernelQtView()

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

    @property
    def open_kernels_configurator_callback(self):
        return None

    @open_kernels_configurator_callback.setter
    def open_kernels_configurator_callback(self, callback):
        self.ui.actionBeam_Kernels.triggered.connect(callback)

    @property
    def add_new_plan_callback(self):
        return None

    @add_new_plan_callback.setter
    def add_new_plan_callback(self, callback):
        self.ui.actionNew_Plan.triggered.connect(callback)

    @property
    def about_callback(self):
        return None

    @about_callback.setter
    def about_callback(self, callback):
        self.ui.actionAbout.triggered.connect(callback)

    @property
    def trip_config_callback(self):
        return None

    @trip_config_callback.setter
    def trip_config_callback(self, callback):
        self.ui.actionTRiP98_Config.triggered.connect(callback)
