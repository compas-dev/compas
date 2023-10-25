********************
Development Workflow
********************

Setup
=====

To set up a developer environment

1. Fork `the repository <https://github.com/compas-dev/compas>`_ and clone the fork. See `Fork a repo <https://help.github.com/articles/fork-a-repo/>`_ for more information.

2. Create a virtual environment using your tool of choice (e.g. `virtualenv`, `conda`, etc).

   .. code-block:: bash

       conda create -n compas-dev python=3.9 --yes
       conda activate compas-dev

3. Install development dependencies:

   .. code-block:: bash

       cd path/to/compas
       pip install -r requirements-dev.txt

4. Make sure all tests pass and the code is free of lint:

   .. code-block:: bash

       invoke lint
       invoke test


Making changes
==============

1. Create a branch for your contributions.

   Prefix your branch name with the type of contribution you are making (e.g. ``feature-``, ``bugfix-``, ``doc-``, etc), followed by a short title of the proposed changes.

   .. code-block::

       git branch feature-new-method
       git checkout feature-new-method


2. Making and pushing changes.

   Go ahead and make a few changes to the project using your favorite text editor. When you're ready to submit your changes, stage and commit your changes. Please use clear commit messages detailing the changes made.
   
   .. code-block:: bash

      git add .
      git commit -m "add functionality X to compas"
      git push origin feature-new-method

   You can continue to make more changes, and take more commit snapshots.

3. Keeping your branch up to date.

   If you are working on a branch for a longer period of time, it is a good idea to keep your branch up to date with the main branch. This way, you can avoid merge conflicts when you submit your changes through a pull request.

   .. code-block:: bash

       git checkout main
       git pull origin main
       git checkout feature-new-method
       git merge main

   If there are any conflicts, you will have to resolve them manually. Once you are done, you can push your changes to your fork.

   .. code-block:: bash

       git push origin feature-new-method


Submitting a PR
===============

.. note::

   The smaller the PR, the easier it is to review and merge. If you are working on a larger feature, consider splitting it up into multiple PRs. This will make it easier for us to review your changes and provide feedback. Alternatively, you can open a draft PR to get feedback on your work in progress.

Once you are done making changes, you have to submit your contribution through a pull request (PR).
The procedure for submitting a PR is the following.


1. Please merge the `main` branch into your feature branch and resolve any conflicts (see above).

2. Make sure all tests still pass, the code is free of lint, and the docstrings compile correctly:

   .. code-block:: bash

        invoke lint
        invoke test
        invoke docs

3. Add yourself to ``AUTHORS.md``.

4. Summarize the changes you made in ``CHANGELOG.md`` in the `Unreleased` section under the most fitting heading (e.g. `Added`, `Changed`, `Removed`).

5. Commit your changes and push your branch to GitHub.

   .. code-block:: bash

       git add .
       git commit -m "add functionality X to compas"
       git push origin feature-new-method

5. Create a `pull request <https://help.github.com/articles/about-pull-requests/>`_.

   * Give your PR a title and describe your change in a few sentences.
   * If your PR fixes an issue, add ``Fixes #123`` to the description, where ``123`` is the issue number.
   * If your PR adds a new feature, add ``New feature`` to the description.
   * If your PR fixes a bug, add ``Bug fix`` to the description.
   * If your PR changes the API, add ``Breaking change`` to the description.
   
6. Wait for the tests to pass and for the code to be reviewed.

   We review pull requests as soon as we can, typically within a week. If you get no review comments within two weeks, feel free to ask for feedback by adding a comment on your PR (this will notify maintainers). Thank you!