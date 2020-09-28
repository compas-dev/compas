***********************
Rhino (Windows and Mac)
***********************

Installing COMPAS for Rhino is very simple.
Just type the following on the command line

.. code-block:: bash

    python -m compas_rhino.install

Optionally, you could provide a Rhino version number (6.0, 7.0).
The default is 6.0.

.. code-block:: bash

    python -m compas_rhino.install -v 6.0

If you installed COMPAS using ``conda``, which is highly recommended, make sure
that the environment in which you installed COMPAS is active when you issue the
above commands.


Install COMPAS packages
=======================

The procedure for installing a COMPAS package in Rhino is similar to installing
COMPAS itself.

.. code-block:: bash

    python -m compas_rhino.install -p compas_fab
