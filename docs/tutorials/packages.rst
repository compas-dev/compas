********************************************************************************
Making a Package
********************************************************************************

Using the **COMPAS** ``cookiecutter`` template we are going to set up a package named ``compas_awesome``.


.. note::

    It is a good idea to create an isolated environment for your package development.
    With ``conda``, managing virtual environments is easy.


Install the cookiecutter
========================

.. code-block:: bash

    $ pip install cookiecutter


Use the cookiecutter
====================

Navigate to the folder where you want to create your package.

.. code-block:: bash

    $ cookiecutter gh:BlockResearchGroup/cookiecutter-compas-package

And then just follow the instructions.
Provide ``compas_awesome`` when asked for the *project_slug*.


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
