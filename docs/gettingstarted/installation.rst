********************************************************************************
Installation
********************************************************************************

.. highlight:: bash

The recommended way to install COMPAS is with `conda <https://conda.io/docs/>`_.
The following commands have to issued on the command line.

.. note::

    On Windows, use the Anaconda Prompt and NOT the Command Prompt.
    On OSX, just use the Terminal app.


First add ``conda-forge`` to the list of channels where ``conda`` looks for packages.

::

    conda config --add channels conda-forge


Install COMPAS in the current environment.

::

    conda install COMPAS


Install a specific version of COMPAS.

::

    conda install COMPAS=0.7.0


Install COMPAS in a separate environment.

::

    conda create -n compas-dev COMPAS


Install COMPAS in a separate environment with a specific version of Python.

::

    conda create -n compas-dev python=3.7 COMPAS


.. note::

    If you install COMPAS in a separate environment (recommended),
    don't forget to activate the environment when you want to use the installed functionality.

    ::

        conda activate compas-dev

