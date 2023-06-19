************
Installation
************

.. rst-class:: lead

COMPAS can be easily installed on multiple platforms,
using popular package managers such as conda or pip.

.. figure:: /_images/installation.gif
     :figclass: figure
     :class: figure-img img-fluid mx-auto


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

    conda create -n research python=3.8 compas

Install COMPAS in an existing environment.

.. code-block:: bash

    conda install -n research compas


Install with pip
================

Install COMPAS using ``pip`` from the Python Package Index.

.. code-block:: bash

    pip install cython --install-option="--no-cython-compile"
    pip install compas

Install an editable version from local source.

.. code-block:: bash

    cd path/to/compas
    pip install -e .

By default, ``planarity`` is marked as an optional requirement for installation with ``pip`` on Windows.
To include ``planarity``, add a conditional to the install command.

.. code-block:: bash

    pip install compas[planarity]

.. code-block:: bash

    pip install -e .[planarity]


Update with conda
=================

Update COMPAS to the latest version with ``conda``.

.. code-block:: bash

    conda update compas

Install a specific version.

.. code-block:: bash

    conda install compas=1.13.3


Update with pip
===============

Update COMPAS to the latest version with ``pip``.

.. code-block:: bash

    pip install --upgrade compas

Install a specific version.

.. code-block:: bash

    pip install compas==1.13.3


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
    pip install compas


Microsoft Visual C++ Build Tools
--------------------------------

The installation with ``pip`` can fail because "Microsoft Visual C++ Build Tools are missing".
To install the Microsoft Visual C++ Build Tools choose one of the options provided
here: https://www.scivision.dev/python-windows-visual-c-14-required/
and just follow the instructions.
Then run the ``pip`` installation commands again.


RuntimeError: The current Numpy installation (...) fails to pass a sanity check
-------------------------------------------------------------------------------

If you see this error, it means latest Numpy 1.19.4 could not init due to a bug from windows.
To avoid it, simply downgrade Numpy by ``pip install numpy==1.19.3``
See the detail of the bug here: https://github.com/numpy/numpy/issues/17726
