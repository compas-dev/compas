.. _installation:

************
Installation
************

.. describe cross-platfrom ness like on homepage


Install in a conda environment (recommended)
============================================

The recommended way to install COMPAS is with `conda <https://conda.io/docs/>`_.


All-in-one
----------

Create an environment named "project", install Python 3.7 and COMPAS (use the ``conda-forge`` channel), say "yes" to all questions asked.

.. code-block:: bash

    conda create -n project python=3.7 COMPAS -c conda-forge --yes


Step-by-Step
------------

1. Create a Python 3.7 environment named "project".
2. Activate the environment.
3. Install COMPAS

.. code-block:: bash

    conda create -n project python=3.7
    conda activate project
    conda install COMPAS -c conda-forge


Verify
------

.. code-block:: bash

    conda activate project
    python
    >>> import compas
    >>> compas.__version__
    '0.15.6'


Install with pip
================

Install a released version.

.. code-block:: bash

    pip install COMPAS


Install an editable version from local source.

.. code-block:: bash

    pip install -e .


Note that the same is possible in combination with ``conda`` environments.

.. code-block:: bash

    conda activate project
    pip install -e .


Known Issues
============

If you encounter a problem that is not described here,
please file an issue using the `Issue Tracker <https://github.com/compas-dev/compas/issues>`_.


Installing Planarity
--------------------

**Problem** The installation process with ``pip`` fails while installing ``planarity``, because ``cython`` is not installed.

Install ``cython`` using ``pip`` (or ``conda``), before installing COMPAS.

.. code-block:: bash

    pip install cython --install-option="--no-cython-compile"
    pip install COMPAS


.. code-block:: bash

    conda install cython
    pip install COMPAS


Microsoft Visual C++ Build Tools
--------------------------------

**Problem** The installation of COMPAS, or a COMPAS package, or any other package, fails because "Microsoft Visual C++ Build Tools are missing".

To install the Microsoft Visual C++ Build Tools choose one of the options provided
here: https://www.scivision.dev/python-windows-visual-c-14-required/
and just follow the instructions.

