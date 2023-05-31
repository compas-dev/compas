********************
Development Workflow
********************

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
