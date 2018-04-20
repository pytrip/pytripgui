import pytest
from pytestqt.qt_compat import qt_api

from pytripgui.main import AppWindow

def test_basics(qtbot):
    assert qt_api.QApplication.instance() is not None
    widget = AppWindow()
    qtbot.addWidget(widget)
    widget.show()

    assert widget.isVisible()
    assert widget.windowTitle() == 'PyTRiPGUI'
