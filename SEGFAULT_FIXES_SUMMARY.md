# Segmentation Fault Debugging Implementation

## Summary

Added comprehensive debugging infrastructure to diagnose and prevent random segmentation faults that occur during test execution, particularly on GitHub Actions CI systems.

## Changes Made

### 1. **Enhanced Test Cleanup** ([tests/conftest.py](tests/conftest.py))

Added aggressive resource cleanup to prevent memory leaks and segfaults:

- **`_cleanup_after_test()` fixture**: Runs after each test to force garbage collection and Qt event processing
- **`pytest_sessionfinish()` hook**: Performs final cleanup after all tests complete, including:
  - Explicit Qt application quit
  - Final garbage collection
  - Status message confirmation
- **Improved `_headless_qt_env()` fixture**: Adds debug environment variables:
  - `QT_DEBUG_PLUGINS=1` - Enable Qt plugin debugging
  - `PYTEST_TIMEOUT=300` - Prevent infinite hangs
  - Core dump handling for Linux

### 2. **CI Workflow Improvements** ([.github/workflows/test.yml](.github/workflows/test.yml))

Enhanced the test workflow with segfault debugging features:

**Smoke tests job:**
- Enable `PYTHONFAULTHANDLER=1` - Python will print traceback on segfault
- Set `PYTEST_TIMEOUT=300` - Prevent hanging tests
- Enable `ulimit -c unlimited` - Allow core dump creation
- Add `-v --tb=short` flags - Verbose output with short tracebacks
- Core dump check after tests

**Normal tests job (Linux):**
- Same debugging configuration as smoke tests
- Enables early detection of platform-specific issues

### 3. **Debug Script** ([debug_segfaults.py](debug_segfaults.py))

Created a command-line tool for local debugging with multiple methods:

```bash
# Run with verbose output and fault handler (recommended)
python debug_segfaults.py --method verbose

# Run with timeout detection
python debug_segfaults.py --method timeout

# Run specific test with gdb debugger (Linux)
python debug_segfaults.py --method gdb --test tests/test_pytripgui.py::test_create_plan_and_field

# Run with valgrind memory checker (Linux, slow)
python debug_segfaults.py --method valgrind
```

### 4. **Documentation** ([DEBUG_SEGFAULTS.md](DEBUG_SEGFAULTS.md))

Comprehensive debugging guide including:

- Root cause analysis of common segfaults
- 7 different debugging methods with examples
- Environment variables for debugging
- Investigation checklist
- Common fixes and references

### 5. **New Dependencies** ([pyproject.toml](pyproject.toml))

Added to dev dependencies:
- `pytest-timeout>=2.1` - Detect hanging/stuck tests
- Updated test marker documentation

## How It Works

### Prevents Segfaults
1. **Garbage collection**: Cleans up Python objects after each test
2. **Qt cleanup**: Explicitly quits Qt application at end of tests
3. **Event processing**: Flushes pending Qt events to prevent dangling references
4. **Core resource cleanup**: Prevents resource leaks that cause memory issues

### Detects Segfaults
1. **Python fault handler**: Prints backtrace when segfault occurs
2. **Verbose output**: Shows exactly which test is running when crash happens
3. **Timeout detection**: Catches tests that hang before crashing
4. **Core dumps**: Linux can create core files for post-mortem analysis

## Testing Locally

The improvements have been tested on:
- Windows 10 with Python 3.14
- All 5 tests pass with improved cleanup
- No segfaults observed with new cleanup code

## Troubleshooting Guide

If you still see segfaults on GitHub Actions:

1. **First**: Check the PYTHONFAULTHANDLER output in logs to see where crash occurs
2. **Second**: Run `debug_segfaults.py --method verbose` locally to reproduce
3. **Third**: Check if it's PyQt5, matplotlib, or pytrip98 C extension related
4. **Fourth**: Run with valgrind on Linux: `debug_segfaults.py --method valgrind`

## Expected Improvements

- **Reduced random failures**: Better cleanup prevents resource exhaustion
- **Better diagnostics**: PYTHONFAULTHANDLER gives exact location of crashes
- **Faster CI**: No more hanging tests thanks to timeout detection
- **Reproducibility**: Can diagnose issues locally with debug script

## Files Modified

1. `tests/conftest.py` - Enhanced cleanup and debug configuration
2. `.github/workflows/test.yml` - Added debug environment variables and core dump handling
3. `pyproject.toml` - Added pytest-timeout dependency
4. `debug_segfaults.py` - New debug script (created)
5. `DEBUG_SEGFAULTS.md` - New debug documentation (created)

## Next Steps if Issues Persist

1. Run tests locally: `python debug_segfaults.py --method verbose`
2. Check Python fault handler output for segfault location
3. Review recent changes to PyQt5, matplotlib, or test code
4. Use `debug_segfaults.py --method valgrind` for detailed memory analysis
5. Consider AddressSanitizer (ASAN) for faster memory error detection
