********************************************************************************
Making a Package
********************************************************************************

Using ``conda``, the **COMPAS** ``cookiecutter`` template, and ``sphinx_compas_theme``,
we are going to set up a package named ``compas_awesome``.


Create a virtual environment
============================

.. code-block:: bash

    $ conda config --add channels conda-forge
    $ conda create -n compas_awesome python=3.6 COMPAS

.. note::

    You can use any name for the conda environment.


Activate the environment
========================

.. code-block:: bash

    $ source activate compas_awesome


Install stuff
=============

.. code-block:: bash

    $ pip install cookiecutter
    $ pip install sphinx_compas_theme


Make a base folder for all your packages
========================================

.. code-block:: bash

    $ mkdir ~/Code/COMPAS-packages
    $ cd ~/Code/COMPAS-packages


Use the cookiecutter
====================

.. code-block:: bash

    $ cookiecutter gh:BlockResearchGroup/cookiecutter-compas-package

And then just follow the instructions.
Provide ``compas_awesome`` when asked for the *project_slug*.


Verify the template
===================

If all went well, the cookiecutter


Install your package
====================

.. code-block:: bash

    $ cd compas_awesome
    $ pip install -r requirements-dev.txt

.. note::

    This will install a few development tools and an editable version of your package.
    This means that all changes you make to the source code will be reflected in
    the installed version of the package.


Build the docs
==============

.. code-block:: bash

    $ invoke docs
    $ open dist/docs/index.html
