from PyQt5.QtWidgets import QApplication, QMainWindow

from pytripgui.app_logic.app_callbacks import AppCallback
from pytripgui.model.main_model import MainModel
from pytripgui.main_window_qt_vc.main_window_view import MainWindowQtView

from pytripgui.plan_executor.trip_config import Trip98ConfigModel

a = QApplication([])


window = MainWindowQtView()
window.show()

model = MainModel()
call = AppCallback(model, window)
model.settings.trip_config = list()

config = Trip98ConfigModel()
config.remote_execution = True
config.host_name = "Hostname"
config.username = "user"
config.password = "pass"
model.settings.trip_config.append(config)

config = Trip98ConfigModel()
config.remote_execution = False
config.host_name = "Hostname"
config.username = "user"
config.password = "pass"
model.settings.trip_config.append(config)


call.on_trip98_config()

exit(a.exec_())
