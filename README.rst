Overview
========

**pytripgui** is graphical user interface (GUI) built around TRiP98 planning system and pytrip package.
It is capable of visualising patient CT data, dose and LET overlays.
pytripgui can make treatment plans using local or remote TRiP98 package.

TRiP98 package is not included here, if you need it, go first to TRiP98 webpage
http://bio.gsi.de/DOCS/TRiP98/NEW/DOCS/trip98.html

pytripgui works under Linux operating system with necessary packages installed, see installation instructions below.

Quick installation guide
------------------------

We recommend that you run a recent Linux distribution. A recent Ubuntu version or Debian Stable/Testing should work,
or any rolling release (archLinux, openSUSE tumbleweed). In this case, be sure you have **python**
and **pythpip** installed.

As a baseline we recommend running python version at least 3.5.
To get them and install system-wide on Debian or Ubuntu, type being logged in as normal user::

   $ sudo pip install python3-pip

To automatically download and install the pytripgui system-wide, type::

    $ sudo pip install pytrip98gui

NOTE: the pip package is named **pytrip98gui**, while the name of project is **pytripgui**.

Start it by calling::

    $ pytripgui

pytripgui currently works in Linux with Python 3.5-3.7. Windows is partially supported.


pytripgui dedicated to python2 users is not supported anymore, if you really know what to do,
then try installing it with::

    $ sudo pip install "pytrip98gui<1.0"



More documentation
------------------

If you would like to download and run the source code of pytripgui,
please see `developer documentation <docs/technical.rst>`__.
