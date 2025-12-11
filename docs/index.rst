=======================================
Welcome to PyTRiP98GUI's documentation!
=======================================

Contents:

.. toctree::
   :maxdepth: 2

   readme
   user_guide
   technical
   authors
   contributing

Release process
---------------

The project publishes pure-Python wheels and a source distribution using a single CI workflow.
On tagged releases, the workflow builds packages with ``python -m build`` and publishes to PyPI,
and generates Sphinx documentation that is deployed to GitHub Pages.
