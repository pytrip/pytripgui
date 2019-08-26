import logging
from pytestqt.qt_compat import qt_api

from pytripgui.main import AppWindow

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_basics(qtbot):
    assert qt_api.QApplication.instance() is not None
    widget = AppWindow()
    qtbot.addWidget(widget)
    widget.show()

    assert widget.view.ui.isVisible()
    assert widget.view.ui.windowTitle() == 'PyTRiPGUI'
