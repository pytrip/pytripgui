from PyQt5.QtWidgets import QApplication, QMainWindow

from pytripgui.app_logic.app_callbacks import AppCallback
from pytripgui.model.main_model import MainModel
from pytripgui.main_window_qt_vc.main_window_view import MainWindowQtView

from pytripgui.plan_executor.trip_config import Trip98ConfigModel
from pytripgui.view.execute_config_view import ExecuteConfigView

a = QApplication([])

window = MainWindowQtView()
window.show()

model = MainModel()

config = Trip98ConfigModel()
config.remote_execution = True
config.name = "name1"
config.host_name = "Hostname"
config.user_name = "user"
config.password = "pass"
model.settings.trip_configs.append(config)

config = Trip98ConfigModel()
config.remote_execution = False
config.name = "name2"
config.trip_path = "trip"
config.wdir_path = "wdir"
model.settings.trip_configs.append(config)

trip = ExecuteConfigView(model.trip_configs, None)
trip.show()

#call = AppCallback(model, window)

#call.on_trip98_config()

exit(a.exec_())
