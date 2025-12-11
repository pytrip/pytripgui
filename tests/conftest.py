import os
import platform

import matplotlib
import pytest


@pytest.fixture(scope="session", autouse=True)
def _headless_qt_env():
    """Ensure tests run without a visible display."""
    if platform.system() == "Linux":
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    os.environ.setdefault("MPLBACKEND", "Agg")
    matplotlib.use(os.environ["MPLBACKEND"])
