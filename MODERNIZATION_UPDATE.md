# PyTRiPGUI - Modernization Update

## Summary of Changes

This update completes the modernization of the PyTRiPGUI project by switching to dynamic versioning and improving the CI/CD pipeline.

### ✅ **Dynamic Versioning with setuptools-scm**

- **Before**: Hard-coded version `1.5.0` in pyproject.toml
- **After**: Dynamic version derived from git tags using `setuptools-scm`

Version is now automatically generated from git history:
- From tags: `1.5.0` (on release tags)
- From commits: `1.5.0.post15+g79eaf67d4.d20251211` (post-release with commit info)

**Configuration**:
```toml
[build-system]
requires = ["setuptools>=64", "setuptools_scm>=8", "wheel"]

[project]
dynamic = ["version"]

[tool.setuptools_scm]
version_scheme = "post-release"
local_scheme = "node-and-date"
write_to = "pytripgui/_version.py"
```

### ✅ **Updated pytrip98 Dependency**

- **Before**: `pytrip98[remote]>=3.7`
- **After**: `pytrip98[remote]>=3.10.1`

Requires at least version 3.10.1 of pytrip98 for full Python 3.14 compatibility.

### ✅ **Removed requirements.txt**

- `requirements.txt` has been completely removed
- All dependencies are now managed exclusively via `pyproject.toml`
- Single source of truth for dependency management

### ✅ **Modern CI/CD with GitHub Actions**

Created `.github/workflows/wheels.yml` with:

**Build Triggers**:
- Manual dispatch: `workflow_dispatch`
- Push to master branch
- On releases (when published)
- Scheduled weekly builds (Tuesdays at 18:46 UTC)

**Build Matrix**:
- **Operating Systems**: Ubuntu, Windows, macOS
- **Python Versions**: 3.9, 3.10, 3.11, 3.12, 3.13, 3.14 (6 versions × 3 OSes = 18 parallel builds)

**Jobs**:
1. **build_sdist**: Creates source distribution (sdist) on Ubuntu
2. **build_wheels**: Builds platform-specific wheels using cibuildwheel
3. **upload_all**: Automatically uploads to PyPI on release

**Features**:
- Parallel builds across OS/Python version matrix for faster CI
- Full git history checkout for setuptools-scm versioning
- Metadata validation with twine
- Automatic PyPI publishing on release
- Build artifact management and preservation

### ✅ **Removed AppVeyor Support**

- Deleted `appveyor.yml` configuration file
- Deleted `appveyor/` directory with deployment scripts
- Completely migrated CI/CD to GitHub Actions

**Rationale**: GitHub Actions is now the standard CI/CD platform and provides native integration with GitHub. AppVeyor was redundant and added maintenance burden.

### 📋 **Files Modified**

| File | Change |
|------|--------|
| `pyproject.toml` | Updated build requirements, made version dynamic, updated pytrip98 to >=3.10.1 |
| `.github/workflows/wheels.yml` | Created - new modern CI/CD pipeline |
| `.gitignore` | Added `pytripgui/_version.py` to ignore generated version file |
| `requirements.txt` | **DELETED** - use pyproject.toml instead |
| `appveyor.yml` | **DELETED** - migrated to GitHub Actions |
| `appveyor/` | **DELETED** - directory with AppVeyor scripts |

### 🔄 **Installation & Testing**

Installation continues to work seamlessly:

```bash
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -e .
```

✅ Verified with Python 3.14.2:
- Module imports successfully
- Dynamic versioning generates correct version strings
- All dependencies resolve correctly

### 📦 **Build Process**

To build wheels locally for testing:

```bash
# Install build dependencies
pip install build setuptools_scm

# Build distributions
python -m build

# Result: dist/*.whl and dist/*.tar.gz
```

### 🚀 **Release Process**

1. Create and push a git tag: `git tag -a v1.5.0 -m "Release 1.5.0"`
2. Push tags: `git push --tags`
3. Create a release on GitHub
4. The wheels workflow automatically:
   - Builds wheels for all OS/Python combinations
   - Uploads to PyPI using trusted publishers

### ⚠️ **Breaking Changes**

None for users. For developers:
- `requirements.txt` no longer exists - use `pip install -e ".[dev]"` instead
- `appveyor.yml` no longer exists - CI/CD is now via GitHub Actions only

### 📝 **Notes**

- The `pytripgui/_version.py` file is auto-generated at build time and should not be committed to git
- Git history and tags are required for proper version calculation
- The generated version file is created only during build/install (not in the repository)

### ✨ **Future Enhancements**

Consider adding to CI/CD:
- Automated changelog generation from git commits
- Sphinx documentation building and hosting
- Code coverage reporting
- Integration with ReadTheDocs for automatic docs deployment
