========
Overview
========

**PyTRiPGUI** is the graphical user interface (GUI) built around the TRiP98 planning system and PyTRiP package.
It is capable of visualising patient CT data, dose and LET overlays.
PyTRiPGUI can make treatment plans using the local or remote TRiP98 package.

The TRiP98 package is not included here. If you need it, first go to `the TRiP98 webpage <http://bio.gsi.de/DOCS/TRiP98/NEW/DOCS/trip98.html>`_.

PyTRiPGUI works under most popular operating systems with necessary packages installed (see installation instructions below).

Installation guide
------------------

PyTRiPGUI currently works on Linux, Windows and macOS with Python 3.6-3.10.

Windows
~~~~~~~

On Windows you can install PyTRiPGUI using the console or the installer. We recommend using the latest installer
that is `available here <https://github.com/pytrip/pytripgui/releases/latest>`_.
To install, download the .exe file and run it. The installer doesn't require preinstalled Python.

Linux and macOS
~~~~~~~~~~~~~~~

We recommend that you run a recent Linux distribution. A recent Ubuntu version or Debian Stable/Testing should work,
or any rolling release (archLinux, openSUSE tumbleweed). In this case, be sure you have **Python**
and **pip** installed.

As a baseline we recommend running Python version at least 3.6.
To get them and install system-wide on Debian or Ubuntu, type being logged in as a normal user::

    $ sudo apt-get install python3 python3-pip

On macOS type::

    $ brew install python3 python3-pip

To automatically download and install the PyTRiPGUI system-wide, type::

    $ pip install pytrip98gui

NOTE: the pip package is named **pytrip98gui**, while the name of the project is **pytripgui**.

Start it by calling::

    $ pytripgui

More documentation
------------------

If you would like to download and run the source code of PyTRiPGUI,
please see :ref:`developer documentation <technical>`.
