import logging
from pytestqt.qt_compat import qt_api

from pytripgui.view.qt_gui import UiMainWindow

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_basics(qtbot):
    assert qt_api.QApplication.instance() is not None
    widget = UiMainWindow()
    qtbot.addWidget(widget)
    widget.show()

    assert widget.isVisible()
    assert widget.windowTitle() == 'PyTRiPGUI'
