import logging

from pytripgui.app_logic.patient_tree import PatientTree
from pytripgui.main_window_qt_vc import MainWindowQtView

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_basics(qtbot):
    view = MainWindowQtView()

    patient_tree = PatientTree(view.ui)
    patient_tree.set_visible(True)

    qtbot.addWidget(view.ui)
    view.show()

    assert view.ui.isVisible()
