********************************************************************************
Contributions
********************************************************************************

Bug reports
===========

When `reporting a bug <https://github.com/compas-dev/compas/issues>`_
please include:

    * Operating system name and version.
    * Any details about your local setup that might be helpful in troubleshooting.
    * Detailed steps to reproduce the bug.


Feature requests and feedback
=============================

The best way to send feedback is to file an issue on
`Github <https://github.com/compas-dev/compas/issues>`_.
If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.


Code contributions
==================

We accept code contributions through pull requests.
In short, this is how that works.

1. Fork `the repository <https://github.com/compas-dev/compas>`_ and clone the fork.
2. Create a virtual environment using your tool of choice (e.g. ``virtualenv``, ``conda``, etc).
3. Install development dependencies:

::

    $ pip install -r requirements-dev.txt


4. Make sure all tests pass:

::

    $ invoke test


5. Start making your changes to the **master** branch (or branch off of it).
6. Make sure all tests still pass:

::

    $ invoke test


7. Add yourself to ``AUTHORS.md``.
8. Commit your changes and push your branch to GitHub.
9. Create a `pull request <https://help.github.com/articles/about-pull-requests/>`_ through the GitHub website.


During development, use `pyinvoke <http://docs.pyinvoke.org/>`_ tasks on the
command line to ease recurring operations:

* ``invoke clean``: Clean all generated artifacts.
* ``invoke check``: Run various code and documentation style checks.
* ``invoke docs``: Generate documentation.
* ``invoke test``: Run all tests and checks in one swift command.
* ``invoke``: Show available tasks.
