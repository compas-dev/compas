********************************************************************************
Making a Rhino plugin
********************************************************************************

.. warning::

    These instructions are a *work in progress* and may not yet perform as advertised :)


Using the COMPAS ``cookiecutter`` template for Rhino Python PlugIns we are going
to set up a plugin named "AwesomePlugIn".


Install cookiecutter
====================

.. code-block:: bash

    $ pip install cookiecutter


Use the cookiecutter template
=============================

.. note::

    Navigate to the folder where you want to keep the source code of your plugin.

.. code-block:: bash

    $ cookiecutter gh:BlockResearchGroup/cookiecutter-compas-package

And then just follow the instructions.
Provide "AwesomePlugIn" when asked for the *plugin_name*.


Install the plugin
==================

**for Rhino on Mac**

.. code-block:: bash

    $ python -m compas_rhinomac.install_plugin <full plugin_name>


**for Rhino**

.. code-block:: bash

    $ python -m compas_rhino.install_plugin <full plugin_name>


.. note::

    To get the full plugin name, you can use the autocompletion of the CommandLine.
    Just type the name of the plugin and then hit *TAB* to get the full name with the
    curly braces and guid.

