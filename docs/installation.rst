************
Installation
************

.. rst-class:: lead

COMPAS is written entirely in Python and can be easily installed
using popular package managers on multiple platforms.


Install with conda
==================

The recommended way to install COMPAS is with `conda <https://conda.io/docs/>`_.
For example, create an environment named ``my-project`` and install COMPAS.

.. code-block:: bash

    conda config --add channels conda-forge
    conda create -n my-project COMPAS

Afterwards, simply activate the environment
and run the following command to check if the installation process was successful.

.. code-block:: bash

    conda activate my-project
    python -m compas

.. code-block:: none

    Yay! COMPAS is installed correctly!

    COMPAS: 0.16.5
    Python: 3.8.2 | packaged by conda-forge | (default, Apr 24 2020, 07:56:27) [Clang 9.0.1 ]


Other installation options
--------------------------

Install COMPAS in an environment with a specific version of Python.

.. code-block:: bash

    conda create -n my-project python=3.7 COMPAS

Install COMPAS in an existing environment.

.. code-block:: bash

    conda install -n my-project COMPAS


Install with pip
================

Install COMPAS using ``pip`` from the Python Package Index.

.. code-block:: bash

    pip install COMPAS

Install an editable version from local source.

.. code-block:: bash

    cd path/to/compas
    pip install -e .

Note that installation with ``pip`` is also possible within a ``conda`` environment.

.. code-block:: bash

    conda activate my-project
    pip install -e .


Known Issues
============

If you encounter a problem that is not described here,
please file an issue using the `Issue Tracker <https://github.com/compas-dev/compas/issues>`_.


Installing Planarity
--------------------

The installation process with ``pip`` can fail while installing ``planarity``, because ``cython`` is not installed.
If this is the case, install ``cython`` using ``pip`` (or ``conda``), before installing COMPAS.

.. code-block:: bash

    pip install cython --install-option="--no-cython-compile"
    pip install COMPAS


Microsoft Visual C++ Build Tools
--------------------------------

The installation with ``pip`` can fail because "Microsoft Visual C++ Build Tools are missing".
To install the Microsoft Visual C++ Build Tools choose one of the options provided
here: https://www.scivision.dev/python-windows-visual-c-14-required/
and just follow the instructions.
Then run the ``pip`` installation commands again.
