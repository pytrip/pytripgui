import logging
from pytestqt.qt_compat import qt_api
from PyQt5.QtWidgets import QMainWindow

from pytripgui.app_logic.patient_tree import PatientTree

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_basics(qtbot):
    assert qt_api.QApplication.instance() is not None
    main_window = QMainWindow()
    patient_tree = PatientTree(main_window)
    patient_tree.show(main_window)
    main_window.show()

    qtbot.addWidget(main_window)
    main_window.show()

    assert main_window.isVisible()
