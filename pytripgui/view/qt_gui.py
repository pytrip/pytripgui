from PyQt5 import QtWidgets, uic
import os


class UiTripConfig(QtWidgets.QDialog):
    def __init__(self):
        super(UiTripConfig, self).__init__()
        ui_path = os.path.join(os.curdir, 'trip_config.ui')
        uic.loadUi(ui_path, self)


class UiFieldDialog(QtWidgets.QDialog):
    def __init__(self):
        super(UiFieldDialog, self).__init__()
        ui_path = os.path.join(os.curdir, 'field.ui')
        uic.loadUi(ui_path, self)


class UiKernelDialog(QtWidgets.QDialog):
    def __init__(self):
        super(UiKernelDialog, self).__init__()
        ui_path = os.path.join(os.curdir, 'kernel.ui')
        uic.loadUi(ui_path, self)


class UiPlanDialog(QtWidgets.QDialog):
    def __init__(self):
        super(UiPlanDialog, self).__init__()
        ui_path = os.path.join(os.curdir, 'plan.ui')
        uic.loadUi(ui_path, self)


class UiMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(UiMainWindow, self).__init__()
        ui_path = os.path.join(os.curdir, 'main_window.ui')
        uic.loadUi(ui_path, self)
