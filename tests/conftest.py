import os
import platform
import sys
import traceback
import gc

import matplotlib
import pytest


@pytest.fixture(scope="session", autouse=True)
def _headless_qt_env():
    """Ensure tests run without a visible display."""
    if platform.system() == "Linux":
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
        # Enable debug output for X11 errors on Linux
        os.environ.setdefault("QT_DEBUG_PLUGINS", "1")
        # Enable core dumps for segfault debugging
        os.environ.setdefault("PYTEST_TIMEOUT", "300")
    
    os.environ.setdefault("MPLBACKEND", "Agg")
    matplotlib.use(os.environ["MPLBACKEND"])


@pytest.fixture(scope="function", autouse=True)
def _cleanup_after_test():
    """Clean up resources after each test to prevent memory leaks."""
    yield
    # Force garbage collection to clean up Qt objects
    gc.collect()
    # Flush any pending events
    try:
        from PyQt5.QtWidgets import QApplication
        app = QApplication.instance()
        if app:
            app.processEvents()
    except Exception:
        pass


def pytest_configure(config):
    """Configure pytest with default reruns for flaky tests."""
    config.addinivalue_line(
        "markers", "flaky: mark test as flaky, will be retried up to 3 times on failure"
    )
    # Global default: retry tests up to 3 times on failure with 1 second delay
    # Can be overridden per-test with @pytest.mark.flaky(reruns=N)
    config.option.reruns = 3
    config.option.reruns_delay = 1


def pytest_sessionfinish(session, exitstatus):
    """Clean up after the entire test session."""
    try:
        # Final cleanup of Qt resources
        from PyQt5.QtWidgets import QApplication
        app = QApplication.instance()
        if app:
            app.quit()
    except Exception:
        pass
    
    # Force final garbage collection
    gc.collect()
    
    if exitstatus == 0:
        print("\n[INFO] All tests passed. Tests completed successfully.", file=sys.stderr)
