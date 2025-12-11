# Debugging Segmentation Faults in PyTRiP GUI

This guide helps diagnose segmentation faults that occur during test execution, particularly on CI systems like GitHub Actions.

## Symptoms
- Tests pass but segfault occurs after test completion
- `Segmentation fault (core dumped)` message appears after pytest finishes
- Random failures on GitHub Actions but not locally

## Root Causes (Common)
1. **PyQt5 cleanup issues** - Qt objects not properly cleaned up
2. **Matplotlib threading** - Graphics operations on wrong thread
3. **C extension memory issues** - pytrip98 C extensions with memory leaks
4. **Resource cleanup timing** - Resources freed before all references gone

## Debugging Methods

### 1. Enable Python Fault Handler (Fastest)
Shows Python traceback when segfault occurs:

```bash
export PYTHONFAULTHANDLER=1
xvfb-run --auto-servernum python -m pytest tests -v
```

### 2. Run with Verbose Output
Catches issues during test execution:

```bash
python -m pytest tests -v --tb=short --capture=no
```

### 3. Use pytest-timeout (Prevents Hangs)
Detects if test processes hang before segfaulting:

```bash
python -m pytest tests -v --timeout=300
```

### 4. Memory Leak Detection with Valgrind (Linux, Slow)
For thorough memory leak detection:

```bash
# Install valgrind
sudo apt-get install valgrind

# Run with suppressions for Python and Qt
valgrind --leak-check=full \
  --show-leak-kinds=all \
  --track-origins=yes \
  --verbose \
  --log-file=valgrind-out.txt \
  --suppressions=/usr/lib/python3*/dist-packages/valgrind-python.supp \
  python -m pytest tests -x  # -x stops at first failure
```

### 5. AddressSanitizer (ASAN) - Faster Memory Detection
For faster memory error detection (requires recompiling Python/extensions):

```bash
ASAN_OPTIONS=detect_leaks=1 python -m pytest tests -v
```

### 6. GDB Interactive Debugging (Linux)
For interactive debugging of segfaults:

```bash
# Install gdb
sudo apt-get install gdb

# Run pytest under gdb
gdb --args python -m pytest tests/test_pytripgui.py::test_create_plan_and_field -v
# Inside gdb, type: run
# When segfault occurs, type: bt (backtrace) to see call stack
```

### 7. Core Dump Analysis (Linux)
Analyze core dump files for detailed crash information:

```bash
# Enable core dumps
ulimit -c unlimited

# Run tests
python -m pytest tests -v

# If core dump created, analyze with gdb
gdb /path/to/python core.<pid>
# Inside gdb, type: bt (backtrace)
```

## Environment Variables for Debugging

```bash
# Python fault handler - prints traceback on segfault
export PYTHONFAULTHANDLER=1

# Qt plugin debugging
export QT_DEBUG_PLUGINS=1

# Matplotlib interactive backend debugging
export MPLBACKEND=TkAgg  # or another backend

# Python memory allocation debugging
export PYTHONMALLOC=malloc_debug

# Verbose Qt warnings
export QT_LOGGING_RULES="*=true"
```

## Recommended CI Workflow

The test.yml workflow has been updated to:

1. **Enable core dumps**: `ulimit -c unlimited`
2. **Enable Python fault handler**: `PYTHONFAULTHANDLER=1`
3. **Add verbose output**: `-v --tb=short` flags to pytest
4. **Increased timeout**: `PYTEST_TIMEOUT=300` for long-running tests
5. **Improved cleanup**: conftest.py now forces garbage collection and Qt cleanup

## Investigation Checklist

When debugging a segfault:

- [ ] Run locally with `PYTHONFAULTHANDLER=1` to get traceback
- [ ] Check if segfault happens consistently or randomly
- [ ] Note which test triggers it or if it's post-test cleanup
- [ ] Review recent changes to PyQt5, matplotlib, or test code
- [ ] Check if issue reproduces with Python version used in CI
- [ ] Look for circular references or unclosed resources
- [ ] Check threading issues (Qt operations on non-main thread)

## Common Fixes

1. **Qt cleanup**: Call `QApplication.instance().quit()` explicitly in conftest.py ✓
2. **Garbage collection**: Add `gc.collect()` after each test ✓
3. **Event processing**: Call `app.processEvents()` to flush pending events ✓
4. **Resource cleanup**: Ensure all GUI resources released in fixtures
5. **Threading**: Ensure Qt operations only on main thread
6. **Matplotlib**: Use `Agg` backend (non-interactive) ✓

## References

- [Python faulthandler module](https://docs.python.org/3/library/faulthandler.html)
- [Valgrind documentation](https://valgrind.org/docs/manual/)
- [PyQt5 memory management](https://doc.qt.io/qt-5/qobject.html#memory-management)
- [GDB Quick Start](https://www.gnu.org/software/gdb/documentation/)
