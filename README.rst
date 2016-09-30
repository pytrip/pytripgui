WHAT IS THIS ?
==============

**pytripgui** is graphical user interface (GUI) built around TRiP98 planning system and pytrip package.
It is capable of visualising patient CT data, dose and LET overlays.
pytripgui can make treatment plans using local or remote TRiP98 package.

TRiP98 package is not included here, if you need it, go first to TRiP98 webpage http://bio.gsi.de/DOCS/TRiP98/NEW/DOCS/trip98.html

pytripgui works under Linux operating system with necessary packages installed, see installation instructions below.

Quick installation guide
------------------------

We recommend that you run a modern Linux distribution, like: **Ubuntu 16.04** or newer, **Debian 9 Stretch** (currently known as testing)
or any updated rolling release (archLinux, openSUSE tumbleweed). In this case, be sure you have **python**
and **python-pip** installed. To get them on Debian or Ubuntu, type being logged in as normal user::

    $ sudo apt-get install python-pip

Next step is to install required packages::

    $ sudo apt-get install python-wxgtk3.0 python-tk

To automatically download and install the pytripgui, type::

    $ sudo pip install pytrip98gui

NOTE: the pip package is named **pytrip98gui**, while the name of project is **pytripgui**.

This command will automatically download and install pytripgui for all users in your system.

Start it by calling::

    $ pytripgui

More detailed instruction will available soon. pytripgui currently works only with Python 2.7 on Linux.
pytripgui does not support Windows and Python3.x (yet).


More documentation
------------------

If you would like to download the code of pytripgui, read first `developer documentation <docs/technical.rst>`__.