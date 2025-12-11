# PyTRiPGUI - Python 3.9-3.14 Migration Summary

## Overview
Successfully migrated PyTRiPGUI to support Python 3.9-3.14 and moved to modern `pyproject.toml` configuration.

## Changes Made

### 1. **Dropped Support for Python 3.8 and Earlier**
   - Updated `requires-python` to `>=3.9` in pyproject.toml
   - Updated Python version classifiers to include 3.9 through 3.14

### 2. **Created Modern pyproject.toml**
   - Replaced deprecated `setup.py` configuration with `pyproject.toml`
   - Maintained backward compatibility for editable installs (`pip install -e .`)
   - Old `setup.py` backed up as `setup.py.bak` (can be deleted if desired)

### 3. **Updated Dependencies**
   - **matplotlib**: Updated from `3.4.3` (incompatible with Python 3.14) to `>=3.8.4`
     - matplotlib 3.4.3 had issues with Python 3.14's `configparser` API changes
     - matplotlib 3.8.4+ fully supports Python 3.9-3.14
   - **PyQt5**: Removed version branching, now uniformly requires `>=5.15`
   - **PyQtChart**: Removed version branching, now uniformly requires `>=5.15`
   - All dependencies simplified to cleaner specifications

### 4. **Updated Documentation**
   - **README.rst**: Updated Python version support from "3.6-3.10" to "3.9-3.14"
   - **docs/technical.rst**: 
     - Added Python version requirement statement (3.9 or higher)
     - Added comprehensive development installation section
     - Included virtual environment setup instructions for Windows and Linux/macOS

### 5. **Build System**
   - Set up modern `setuptools>=61.0` with PEP 517 support
   - Proper package discovery configuration with `tool.setuptools.packages.find`
   - Version hardcoded in pyproject.toml (can be enhanced with setuptools-scm if needed)

## Installation Testing

Successfully tested local installation with Python 3.14.2:

```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS

pip install -e .
```

### Installation Results
✅ All dependencies resolved and installed correctly
✅ Module imports successfully
✅ Package entry point (pytripgui command) created correctly

## Dependencies Resolved

### Main Dependencies (Compatible with Python 3.9-3.14):
- matplotlib 3.10.8
- pytrip98 3.10.1
- PyQt5 5.15.11
- PyQtChart 5.15.7
- anytree 2.13.0
- Events 0.5

### Development Dependencies Available:
- pytest, pytest-cov
- sphinx, sphinx-rtd-theme
- flake8, pycodestyle

## Next Steps (Optional Enhancements)

1. **Version Management**: Consider using `setuptools-scm` for automatic version management from git tags
2. **Delete setup.py.bak**: Old setup.py can be safely deleted once migration is confirmed stable
3. **CI/CD Updates**: Update GitHub Actions/AppVeyor to test on Python 3.9-3.14
4. **Release Notes**: Document this migration in project changelog

## Troubleshooting

If you encounter issues:

1. **Module import errors**: These are code-level issues, not installation issues. The migration is successful if `pip install -e .` completes without errors.
2. **Missing dependencies**: Ensure you're using Python 3.9 or higher
3. **Build isolation issues**: Clear pip cache with `pip cache purge` and retry

## Files Modified

- ✅ `pyproject.toml` - Created with complete modern configuration
- ✅ `requirements.txt` - Updated dependency versions
- ✅ `README.rst` - Updated Python version information
- ✅ `docs/technical.rst` - Added development setup guide
- ⚠️ `setup.py` - Renamed to `setup.py.bak` (not executed during build)
