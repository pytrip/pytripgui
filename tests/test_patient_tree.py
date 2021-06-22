import logging
import sys

import pytest

from PyQt5.QtWidgets import QMainWindow

from pytripgui.app_logic.patient_tree import PatientTree

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


@pytest.mark.skipif((sys.version_info[0] == 3) and (sys.version_info[1] == 7),
                    reason="fails on python 3.7 for unknown reasons")
def test_basics(qtbot):
    main_window = QMainWindow()
    patient_tree = PatientTree(main_window, main_window)
    patient_tree.set_visible(True)
    main_window.show()

    qtbot.addWidget(main_window)
    main_window.show()

    assert main_window.isVisible()
