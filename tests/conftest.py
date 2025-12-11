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


def pytest_configure(config):
    """Configure pytest with default reruns for flaky tests."""
    config.addinivalue_line(
        "markers", "flaky: mark test as flaky, will be retried up to 3 times on failure"
    )
    # Global default: all tests are retried up to 3 times on failure with 1 second delay
    # The flaky marker is registered for documentation, but does not control rerun behavior.
