.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/pytrip/pytripgui/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Issues
~~~~~~

There are two types of issues: bugs and features. They are open to everyone.

Write Documentation
~~~~~~~~~~~~~~~~~~~

`PyTRiPGUI` could always use more documentation, whether as part of the
official pytripgui docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

| The best way to send feedback is to file an issue at
| https://github.com/pytrip/pytripgui/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome. :)

Get Started!
------------

Ready to contribute? Here's how to set up `PyTRiPGUI` for local development.

1. Fork the `pytripgui` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/pytripgui.git

3. Install your local copy into a virtualenv. This is how you set up your fork for local development::

    $ cd pytripgui/
    $ python -m venv directory_to_create_venv

4. Activate newly created virtual environment:

  On Linux::

    $ source directory_to_create_venv/bin/activate

  On Windows::

    $ directory_to_create_venv\Scripts\activate.bat

5. Finally install all dependencies needed by your package to develop the code::

    $ python setup.py develop

6. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

Now you can make your changes locally.

7. (optional) When you're done making changes, you can check locally that your changes pass flake8 and the tests,
including testing other Python versions with pytest::

    $ flake8 pytripgui tests
    $ pytest tests

To get flake8 and pytest, just pip install them into your virtual environment.

8. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

9. Submit a pull request through the GitHub website, following our Pull Request Guidelines.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring.
3. The pull request should work for all supported Python versions and operating systems. Check
   https://github.com/pytrip/pytripgui/actions
   and make sure that the automated tests pass.
