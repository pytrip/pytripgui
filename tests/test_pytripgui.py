import logging

from pytripgui.view.qt_gui import UiMainWindow

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_basics(qtbot):
    widget = UiMainWindow()
    qtbot.addWidget(widget)
    widget.show()

    assert widget.isVisible()
    assert widget.windowTitle() == 'PyTRiPGUI'
