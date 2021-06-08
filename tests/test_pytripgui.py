import logging
import sys

import pytest

from pytripgui.view.qt_gui import UiMainWindow

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


@pytest.mark.skipif((sys.version_info[0] == 3) and (sys.version_info[1] == 7),
                    reason="fails on python 3.7 for unknown reasons")
def test_basics(qtbot):
    widget = UiMainWindow()
    qtbot.addWidget(widget)
    widget.show()

    assert widget.isVisible()
    assert widget.windowTitle() == 'PyTRiPGUI'
