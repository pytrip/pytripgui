from PyQt5.QtWidgets import QApplication, QMainWindow

from pytripgui.app_logic.app_callbacks import AppCallback
from pytripgui.model.main_model import MainModel
from pytripgui.main_window_qt_vc.main_window_view import MainWindowQtView


a = QApplication([])


window = MainWindowQtView()
window.show()

model = MainModel()
call = AppCallback(model, window)
call.on_trip98_config()

exit(a.exec_())
