import os

from PyQt5 import QtWidgets, uic

current_directory = os.path.dirname(os.path.realpath(__file__))


class UiTripConfig(QtWidgets.QDialog):
    def __init__(self):
        super(UiTripConfig, self).__init__()
        ui_path = os.path.join(current_directory, 'trip_config.ui')
        uic.loadUi(ui_path, self)


class UiFieldDialog(QtWidgets.QDialog):
    def __init__(self):
        super(UiFieldDialog, self).__init__()
        ui_path = os.path.join(current_directory, 'field.ui')
        uic.loadUi(ui_path, self)


class UiKernelDialog(QtWidgets.QDialog):
    def __init__(self):
        super(UiKernelDialog, self).__init__()
        ui_path = os.path.join(current_directory, 'kernel.ui')
        uic.loadUi(ui_path, self)


class UiPlanDialog(QtWidgets.QDialog):
    def __init__(self):
        super(UiPlanDialog, self).__init__()
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
