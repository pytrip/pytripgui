===========
PyTRiP98GUI
===========

**PyTRiPGUI** is the graphical user interface (GUI) built around the TRiP98 planning system and PyTRiP package.
It is capable of visualising patient CT data, dose and LET overlays.
PyTRiPGUI can make treatment plans using the local or remote TRiP98 package.

The TRiP98 package is not included here. If you need it, first go to `the TRiP98 webpage <http://bio.gsi.de/DOCS/TRiP98/NEW/DOCS/trip98.html>`_.

Quick installation guide
------------------------

PyTRiPGUI currently works on Linux, Windows and macOS with Python 3.9-3.14.

Windows
~~~~~~~

On Windows you can install PyTRiPGUI using the console or the installer. We recommend using the latest installer
that is `available here <https://github.com/pytrip/pytripgui/releases/latest>`_.
To install, download the .exe file and run it. The installer doesn't require preinstalled Python.

Linux and macOS
~~~~~~~~~~~~~~~

We recommend that you run a recent Linux distribution with Python version at least 3.9.

To automatically download and install the PyTRiPGUI system-wide, type::

    $ pip install pytrip98gui

NOTE: the pip package is named **pytrip98gui**, while the name of the project is **pytripgui**.

Start it by calling::

    $ pytripgui

More documentation
------------------

For more information, please see the `detailed documentation <https://pytrip.github.io/pytripgui/>`_.

Release and packaging
---------------------

PyTRiPGUI publishes pure-Python wheels and source distributions via a unified GitHub Actions workflow.
On releases, the workflow builds wheels/sdist and publishes them to PyPI, and it builds Sphinx HTML docs and deploys them to GitHub Pages.
There is no longer any use of cibuildwheel; packaging is performed using `python -m build`.
