.. _cad_rhino:
********************************************************************************
Rhino
********************************************************************************

.. highlight:: bash


*Installing* COMPAS for Rhino is very simple.
Just type the following on the command line

::

    $ python -m compas_rhino.install


Optionally, you could provide a Rhino version number (``5.0, 6.0``).
The default is ``6.0``.

::

    $ python -m compas_rhino.install -v 6.0


.. note::

    On Windows, use the "Anaconda Prompt" instead of the "Command Prompt", and make
    sure to run it as administrator.

    On Mac, use the Terminal.

If you installed COMPAS using ``conda``, which is highly recommended, make sure
that the environment in which you installed COMPAS is active when you issue the
above commands.


Install COMPAS packages
=======================

The procedure for installing a COMPAS package in Rhino is similar to installing
COMPAS itself.

.. code-block:: bash

    $ python -m compas_rhino.install -p compas_fab


Working with virtual environments
=================================

