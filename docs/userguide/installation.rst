************
Installation
************

.. rst-class:: lead

COMPAS can be easily installed on multiple platforms,
using popular package managers such as conda or pip.

Install with conda (recommended)
================================

Create an environment named ``research`` and install COMPAS from the package channel ``conda-forge``.

.. code-block:: bash

    conda create -n research -c conda-forge compas

Activate the environment.

.. code-block:: bash

    conda activate research

Verify that the installation was successful.

.. code-block:: bash

    python -m compas

.. code-block:: none

    Yay! COMPAS is installed correctly!


Installation options
--------------------

Install COMPAS in an environment with a specific version of Python.

.. code-block:: bash

    conda create -n research python=3.9 compas

Install COMPAS in an existing environment.

.. code-block:: bash

    conda install -n research compas


Install with pip
================

Install COMPAS using ``pip`` from the Python Package Index.

.. code-block:: bash

    pip install compas

Install an editable version from local source.

.. code-block:: bash

    cd path/to/compas
    pip install -e .


Update with conda
=================

Update COMPAS to the latest version with ``conda``.

.. code-block:: bash

    conda update compas

Install a specific version.

.. code-block:: bash

    conda install compas=1.17.9


Update with pip
===============

Update COMPAS to the latest version with ``pip``.

.. code-block:: bash

    pip install --upgrade compas

Install a specific version.

.. code-block:: bash

    pip install compas==1.17.9
