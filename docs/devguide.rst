===============
Developer Guide
===============

.. frame contributions within broader gompas goals

.. give overview of contributionn procedure(s)

.. differentiate between code, documentation, package ...

.. making your own package (contrinuting a package) is a different type of contribution


Dev Install
===========

.. code-block:: bash

    conda create -n project python=3.7


.. code-block:: bash

    conda activate project


.. code-block:: bash

    cd path/to/compas/repo


.. code-block:: bash

    pip install -r requirements-dev.txt


Getting Started
===============

We accept code contributions through pull requests.
In short, this is how that works.

1. Fork [the repository](https://github.com/compas-dev/compas) and clone the fork.
2. Create a virtual environment using your tool of choice (e.g. `virtualenv`, `conda`, etc).
3. Install development dependencies:

   ```bash
   pip install -r requirements-dev.txt
   ```

4. Make sure all tests pass:

   ```bash
   invoke test
   ```

5. Start making your changes to the **master** branch (or branch off of it).
6. Make sure all tests still pass:

   ```bash
   invoke test
   ```

7. Add yourself to `AUTHORS.md`.
8. Commit your changes and push your branch to GitHub.
9. Create a [pull request](https://help.github.com/articles/about-pull-requests/) through the GitHub website.

During development, use [pyinvoke](http://docs.pyinvoke.org/) tasks on the
command line to ease recurring operations:

* `invoke clean`: Clean all generated artifacts.
* `invoke check`: Run various code and documentation style checks.
* `invoke docs`: Generate documentation.
* `invoke test`: Run all tests and checks in one swift command.


Code Structure
==============


Documentation
=============


Publishing
==========



