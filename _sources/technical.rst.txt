=========
pytripgui
=========

.. image:: https://img.shields.io/pypi/v/pytripgui.svg
        :target: https://pypi.python.org/pypi/pytrip98gui


.. image:: https://readthedocs.org/projects/pytripgui/badge/?version=latest
        :target: https://readthedocs.org/projects/pytripgui/?badge=latest
        :alt: Documentation Status

========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - |appveyor|
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/pytripgui/badge/?style=flat
    :target: https://readthedocs.org/projects/pytripgui
    :alt: Documentation Status

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/grzanka/pytripgui?branch=master&svg=true
    :alt: Appveyor Build Status
    :target: https://ci.appveyor.com/project/grzanka/pytripgui

.. |version| image:: https://img.shields.io/pypi/v/pytrip98gui.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/pytrip98gui

.. |ghactions| image:: https://github.com/pytrip/pytripgui/actions/workflows/test.yml/badge.svg
    :alt: Github Actions
    :target: https://github.com/pytrip/pytripgui/actions/workflows/test.yml

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

Stable version ::

    pip install pytrip98gui

Latest unstable version, directly from GIT repository::

    pip install git+https://github.com/pytrip/pytripgui.git

To uninstall, simply use::

    pip uninstall pytrip98gui

Running pytripgui
=================

To run stable version installed using pip manager, simply type:
        $ pytripgui

To run unstable, development version of pytripgui (when working with source code), type:
        $ python -m pytripgui.main

Documentation
=============

https://pytripgui.readthedocs.io/


Features
--------

* TODO

History
-------

* earliest mention of the pytrip project dates back to 2010 http://willworkforscience.blogspot.com/2010/12/happy-new-year.html

* 2012-2013 pytrip code with experimental GUI is developed by Niels Bassler and Jakob Toftegaard, code is hosted in SVN repository at Aarhus University (https://svn.nfit.au.dk/trac/pytrip)

  * state of the code in late 2013 can be seen here: https://github.com/pytrip/pytrip/commit/54e2d00d41138431c1c2b69cc6136f87cf4831b8
  * pytrip works with python 2.x, GUI is based on wxwidgets library
  * pytrip (including experimental GUI) was denoted at v0.1
  * functionality of GUI at that moment can be seen in video https://www.youtube.com/embed/6ZqcJ6OZ598

* 2014 Manuscript published:

  * Toftegaard J, Petersen JB, Bassler N. PyTRiP-a toolbox and GUI for the proton/ion therapy planning system TRiP. In Journal of Physics: Conference Series 2014 Mar 24 (Vol. 489, No. 1, p. 012045). https://doi.org/10.1088/1742-6596/489/1/012045

* 2014-2016 pytrip code (including GUI) is publicly available as a SourceForge project (https://sourceforge.net/projects/pytrip/)

  *  Jakob Toftegaard issued several commits, Toke Printz included some fixes (https://github.com/pytrip/pytrip/commit/d6dedb8b5e309f33e06fb766542345064348e7e0)

* 28.08.2016 pytrip (including GUI) is migrated to GIT at Github repository (https://github.com/pytrip/pytrip)

  * pytripgui is extracted to a separate project (https://github.com/pytrip/pytripgui)
  * Leszek Grzanka joins the developer team

* 08.05.2018 pytripgui is migrated from wxwidgets to Qt5 framework (https://github.com/pytrip/pytripgui/commit/cb27fc909d132ce5f7a5e0be5df2dbbfd64e6c1d)

  * GUI shifts completely from python 2.x to python 3.x

* 04.2019 Łukasz Jeleń joins developer team, introducing MVC architecture in the project

* 06.2021 Arkadiusz Ćwikła, Joanna Fortuna, Michał Krawczyk and Mateusz Łaszczyk join project (part of a bachelor thesis at the AGH University)


Credits
-------

 * TODO