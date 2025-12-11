# Quick Reference: Segfault Debugging

## For GitHub Actions Maintainers

The workflow now automatically:
1. ✅ Enables `PYTHONFAULTHANDLER=1` - prints backtrace on crash
2. ✅ Enables `QT_DEBUG_PLUGINS=1` - verbose Qt debugging
3. ✅ Sets `PYTEST_TIMEOUT=300` - prevents hanging tests
4. ✅ Enables core dumps - for post-mortem analysis
5. ✅ Uses improved test cleanup - prevents resource leaks

**No action needed** - these run automatically on every test.

## For Local Debugging

### Quick Debug (Windows/Mac/Linux)
```bash
python debug_segfaults.py --method verbose
```

### Timeout Detection (Windows/Mac/Linux)
```bash
python debug_segfaults.py --method timeout
```

### Linux Interactive Debugging with GDB
```bash
python debug_segfaults.py --method gdb --test tests/test_pytripgui.py::test_create_plan_and_field
```

### Linux Memory Analysis with Valgrind (Slow)
```bash
# Install valgrind first
sudo apt-get install valgrind

# Run memory check
python debug_segfaults.py --method valgrind
```

## Manual Testing with Fault Handler

```bash
# Enable Python fault handler
export PYTHONFAULTHANDLER=1

# Run tests
python -m pytest tests -v

# If segfault occurs, you'll see:
# Fatal Python error: Segmentation fault
# [backtrace will be shown here]
```

## Files Added/Modified

**New files:**
- `debug_segfaults.py` - Debug helper script
- `DEBUG_SEGFAULTS.md` - Detailed debugging guide
- `SEGFAULT_FIXES_SUMMARY.md` - Implementation summary

**Modified files:**
- `tests/conftest.py` - Added aggressive cleanup
- `.github/workflows/test.yml` - Added debugging environment variables
- `pyproject.toml` - Added pytest-timeout dependency

## What's Fixed

### Root Causes Addressed
1. **PyQt5 cleanup** - Now explicitly quits Qt application at session end
2. **Memory leaks** - Forces garbage collection after each test
3. **Dangling resources** - Flushes Qt events to complete cleanup
4. **Resource exhaustion** - Prevents accumulated resource leaks

### CI Improvements
1. **Better diagnostics** - PYTHONFAULTHANDLER prints exact location
2. **Segfault detection** - Core dump checking after tests
3. **Timeout prevention** - 300-second timeout prevents hanging
4. **Verbose logging** - `-v --tb=short` shows exactly what's running

## Testing It Works

Run the test suite locally:
```bash
python -m pytest tests -v --tb=short
```

You should see:
```
collected 5 items
tests/test_kernel_dialog.py::test_basics PASSED
tests/test_patient_tree.py::test_basics PASSED
tests/test_pytripgui.py::test_basics PASSED
tests/test_pytripgui.py::test_open_voxelplan PASSED
tests/test_pytripgui.py::test_create_plan_and_field PASSED

[INFO] All tests passed. Tests completed successfully.
```

## Common Issues & Solutions

**Q: Still seeing segfaults on CI?**
A: Check PYTHONFAULTHANDLER output in logs to see where it crashes. Run `python debug_segfaults.py --method verbose` locally.

**Q: Tests hanging?**
A: New `PYTEST_TIMEOUT=300` should catch these. If still happening, run with `--timeout=60` for shorter timeout.

**Q: Specific test crashes?**
A: Use `python debug_segfaults.py --method gdb --test tests/test_pytripgui.py::test_name` on Linux.

**Q: Memory leak suspected?**
A: Run `python debug_segfaults.py --method valgrind` on Linux (slow but thorough).

## Support Resources

- Full guide: [DEBUG_SEGFAULTS.md](DEBUG_SEGFAULTS.md)
- Implementation details: [SEGFAULT_FIXES_SUMMARY.md](SEGFAULT_FIXES_SUMMARY.md)
- Test configuration: [tests/conftest.py](tests/conftest.py)
- CI workflow: [.github/workflows/test.yml](.github/workflows/test.yml)
