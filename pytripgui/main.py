import sys

from PyQt5.QtWidgets import QMainWindow, QApplication

from controller.main_cont import MainController
from view.main_window import Ui_MainWindow


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()


app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())
