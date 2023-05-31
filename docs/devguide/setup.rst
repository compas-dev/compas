*****
Setup
*****

To set up a developer environment

1. Fork `the repository <https://github.com/compas-dev/compas>`_ and clone the fork.
2. Create a virtual environment using your tool of choice (e.g. `virtualenv`, `conda`, etc).

   .. code-block:: bash

       conda create -n compas-dev python=3.8 cython --yes
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
