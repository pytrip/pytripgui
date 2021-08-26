import os

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt

current_directory = os.path.dirname(os.path.realpath(__file__))


class UiTripConfig(QtWidgets.QDialog):
    def __init__(self):
        super(UiTripConfig, self).__init__()
        ui_path = os.path.join(current_directory, 'trip_config.ui')
        uic.loadUi(ui_path, self)


class UiFieldDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(UiFieldDialog, self).__init__(parent)
        ui_path = os.path.join(current_directory, 'field.ui')
        uic.loadUi(ui_path, self)


class UiExecuteDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(UiExecuteDialog, self).__init__(parent)
        ui_path = os.path.join(current_directory, 'execute.ui')
        uic.loadUi(ui_path, self)


class UiExecuteConfigDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(UiExecuteConfigDialog, self).__init__(parent)
        ui_path = os.path.join(current_directory, 'execute_config.ui')
        uic.loadUi(ui_path, self)


class UiKernelDialog(QtWidgets.QDialog):
    def __init__(self):
        super(UiKernelDialog, self).__init__()
        ui_path = os.path.join(current_directory, 'kernel.ui')
        uic.loadUi(ui_path, self)


class UiPlanDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(UiPlanDialog, self).__init__(parent)
        ui_path = os.path.join(current_directory, 'plan.ui')
        uic.loadUi(ui_path, self)


class UiMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(UiMainWindow, self).__init__()
        ui_path = os.path.join(current_directory, 'main_window.ui')
        uic.loadUi(ui_path, self)
        self.setWindowTitle("PyTRiPGUI")


class UiViewCanvas(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(UiViewCanvas, self).__init__(parent)
        ui_path = os.path.join(current_directory, 'viewcanvas.ui')
        uic.loadUi(ui_path, self)


class UiAddPatient(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(UiAddPatient, self).__init__(parent)
        ui_path = os.path.join(current_directory, 'add_patient.ui')
        uic.loadUi(ui_path, self)

        self._create_empty_callback = None
        self._open_voxelplan_callback = None
        self._open_dicom_callback = None

        self.accept_buttonBox.rejected.connect(self.reject)

    def show(self):
        self.exec_()

    @property
    def on_create_empty(self):
        return None

    @on_create_empty.setter
    def on_create_empty(self, callback):
        self._create_empty_callback = callback
        self.createEmpty_pushButton.clicked.connect(self._create_empty_internal_callback)

    def _create_empty_internal_callback(self):
        self.hide()
        self._create_empty_callback()
        self.reject()

    @property
    def on_open_voxelplan(self):
        return None

    @on_open_voxelplan.setter
    def on_open_voxelplan(self, callback):
        self._open_voxelplan_callback = callback
        self.openVoxelplan_pushButton.clicked.connect(self._on_open_voxelplan_internal_callback)

    def _on_open_voxelplan_internal_callback(self):
        self._open_voxelplan_callback()
        self.reject()

    @property
    def on_open_dicom(self):
        return None

    @on_open_dicom.setter
    def on_open_dicom(self, callback):
        self._open_dicom_callback = callback
        self.openDicom_pushButton.clicked.connect(self._on_open_dicom_internal_callback)

    def _on_open_dicom_internal_callback(self):
        self._open_dicom_callback()
        self.reject()


class EmptyPatientDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(EmptyPatientDialog, self).__init__(parent)
        ui_path = os.path.join(current_directory, 'empty_patient.ui')
        uic.loadUi(ui_path, self)

        self.setWindowFlags(Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint)
