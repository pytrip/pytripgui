.. _technical:

=======================
Developer documentation
=======================

Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - tests
      - |ghactions|
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|


.. |ghactions| image:: https://github.com/pytrip/pytripgui/actions/workflows/test.yml/badge.svg
    :alt: Github Actions
    :target: https://github.com/pytrip/pytripgui/actions/workflows/test.yml

.. |version| image:: https://img.shields.io/pypi/v/pytrip98gui.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/pytrip98gui

.. |downloads| image:: https://img.shields.io/pypi/dm/pytrip98gui.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/pytrip98gui

.. |wheel| image:: https://img.shields.io/pypi/wheel/pytrip98gui.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/pytrip98gui

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pytrip98gui.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/pytrip98gui

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/pytrip98gui.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/pytrip98gui

.. end-badges


Installation
============

Requirements
~~~~~~~~~~~~

- Python 3.9 or higher
- Git

Stable version ::

    pip install pytrip98gui

Latest unstable version, directly from GIT repository::

    pip install git+https://github.com/pytrip/pytripgui.git

Development Installation (from source)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To work with the project locally, clone the repository and install in editable mode::

    git clone https://github.com/pytrip/pytripgui.git
    cd pytripgui
    python -m venv venv
    
On Windows::

    venv\Scripts\activate

On Linux/macOS::

    source venv/bin/activate

Then install in editable mode with development dependencies::

    pip install -e ".[dev]"

To uninstall, simply use::

    pip uninstall pytrip98gui

Running pytripgui
=================

To run stable version installed using pip manager, simply type::

    pytripgui

To run unstable, development version of pytripgui (when working with source code), type::

    python -m pytripgui.main

Building the Windows installer
==============================

To create the Windows installer locally, you need Python 3.14 on Windows, PyInstaller, and Inno Setup 6+. All commands below should be run from the repository root.

1. Create/activate a virtual environment and install build tools::

    python -m venv .venv
    .venv\Scripts\activate
    python -m pip install --upgrade pip
    python -m pip install . pyinstaller

2. Install Inno Setup (for example)::

    choco install innosetup -y

3. Build the frozen application::

    python -m PyInstaller main.spec

   The spec script modifies the matplotlib backend configuration, generates a `VERSION` file in `build/` that is then bundled at the root of the frozen application, and updates `win_innosetup.iss` with the detected version and platform information.

4. Build the installer executable::

    "C:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe" win_innosetup.iss

The final installer lands in `dist/installer/` (for example `pytripgui_<version>_win_64bit_setup.exe`), while the unpacked PyInstaller build lives in `dist/pytripgui/`.

History
=======

* The earliest mention of the pytrip project dates back to 2010: http://willworkforscience.blogspot.com/2010/12/happy-new-year.html

* 2012-2013: pytrip code with an experimental GUI is developed by Niels Bassler and Jakob Toftegaard. The code is hosted in an SVN repository at Aarhus University (https://svn.nfit.au.dk/trac/pytrip)

  * State of the code in late 2013 can be seen here: https://github.com/pytrip/pytrip/commit/54e2d00d41138431c1c2b69cc6136f87cf4831b8
  * pytrip is compatible with Python 2.x; the GUI is based on the wxWidgets library
  * pytrip (including experimental GUI) is designated as v0.1
  * functionality of GUI at that moment can be seen in video https://www.youtube.com/embed/6ZqcJ6OZ598

* 2014: Manuscript published

  * Toftegaard J, Petersen JB, Bassler N. PyTRiP—a toolbox and GUI for the proton/ion therapy planning system TRiP. Journal of Physics: Conference Series 2014 Mar 24 (Vol. 489, No. 1, p. 012045). https://doi.org/10.1088/1742-6596/489/1/012045

* 2014-2016: pytrip code (including GUI) is publicly available as a SourceForge project (https://sourceforge.net/projects/pytrip/)

  * Jakob Toftegaard contributed several commits; Toke Printz added fixes (https://github.com/pytrip/pytrip/commit/d6dedb8b5e309f33e06fb766542345064348e7e0)

* August 28, 2016: pytrip (including GUI) is migrated to Git and hosted on GitHub (https://github.com/pytrip/pytrip)

  * pytripgui is extracted as a separate project (https://github.com/pytrip/pytripgui)
  * Leszek Grzanka joins the development team

* May 8, 2018: pytripgui is migrated from wxWidgets to the Qt5 framework (https://github.com/pytrip/pytripgui/commit/cb27fc909d132ce5f7a5e0be5df2dbbfd64e6c1d)

  * GUI transitions completely from Python 2.x to Python 3.x

* April 2019: Łukasz Jeleń joins the development team, introducing MVC architecture to the project

* June 2021: Arkadiusz Ćwikła, Joanna Fortuna, Michał Krawczyk, and Mateusz Łaszczyk join the project as part of a bachelor's thesis at AGH University

* December 2025: Leszek Grzanka and Niels Bassler undertake efforts to revive the project after 3.5 years of stalled development, modernizing dependencies, fixing installation issues, and adding new features