********
Workflow
********

Setup
=====

To set up a developer environment

1. Fork `the repository <https://github.com/compas-dev/compas>`_ and clone the fork.
2. Create a virtual environment using your tool of choice (e.g. `virtualenv`, `conda`, etc).

   .. code-block:: bash

       conda create -n compas-dev python=3.11 --yes
       conda activate compas-dev

3. Install development dependencies:

   .. code-block:: bash

       cd path/to/compas
       pip install -r requirements-dev.txt

4. Make sure all tests pass and the code is free of lint:

   .. code-block:: bash

       invoke lint
       invoke test

5. Create a branch for your contributions.

   .. code-block::

       git branch title-proposed-changes
       git checkout title-proposed-changes

6. Start making changes!

Submitting a PR
===============

Once you are done making changes, you have to submit your contribution through a pull request (PR).
The procedure for submitting a PR is the following.

1. Make sure all tests still pass, the code is free of lint, and the docstrings compile correctly:

   .. code-block:: bash

        invoke lint
        invoke test
        invoke docs

2. Add yourself to ``AUTHORS.md``.
3. Summarize the changes you made in ``CHANGELOG.md``.
4. Commit your changes and push your branch to GitHub.
5. Create a `pull request <https://help.github.com/articles/about-pull-requests/>`_.
