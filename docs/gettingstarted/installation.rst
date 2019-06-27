********************************************************************************
Installation
********************************************************************************

.. highlight:: bash


The recommended way to install COMPAS is with `conda <https://conda.io/docs/>`_.

Add the ``conda-forge`` package channel.

::

    $ conda config --add channels conda-forge


Install COMPAS in the current environment

::

    $ conda install COMPAS


Install a specific version of COMPAS

::

    $ conda install COMPAS=0.7.0


Install COMPAS in a separate environment

::

    $ conda create -n compas-dev COMPAS


Install COMPAS in a separate environment with a specific version of Python

::

    $ conda create -n compas-dev python=3.7 COMPAS


.. note::

    If you install COMPAS in a separate environment (recommended),
    don't forget to activate the environment when you want to use the installed functionality.

    ::

        $ conda activate compas-dev

