.. _gs-rhino:

***********************
Rhino (Windows and Mac)
***********************

.. rst-class:: lead

COMPAS is backward compatible with IronPython 2.7
and can therefore be used in Rhino, both on Windows and on Mac.

.. .. figure:: /_images/install_rhino.gif
..      :figclass: figure
..      :class: figure-img img-fluid mx-auto


Install COMPAS in Rhino
=======================

.. .. figure:: /_images/install_rhino.gif
..      :figclass: figure
..      :class: figure-img img-fluid mx-auto

If you installed COMPAS using ``conda``, which is highly recommended,
first activate the environment containing the COMPAS installation you want to make available in Rhino.
For example, if the name of the environment is ``research``

.. code-block:: bash

    conda activate research

After that, installing COMPAS in Rhino is very simple.
Just type the following on the command line

.. code-block:: bash

    python -m compas_rhino.install

Optionally, you could provide a Rhino version number (6.0, 7.0).
The default is 6.0.

.. code-block:: bash

    python -m compas_rhino.install -v 6.0


Install COMPAS packages in Rhino
================================

The procedure for installing a COMPAS plugin or extension package in Rhino
is similar to installing COMPAS itself. For example, if you want to install ``compas_fab``

.. code-block:: bash

    python -m compas_rhino.install -p compas_fab

Note, however, that this will only install ``compas_fab``.
If you want to install the core packages as well as ``compas_fab``,
you have to do one of the following.

.. code-block:: bash

    python -m compas_rhino.install
    python -m compas_rhino.install -p compas_fab

.. code-block:: bash

    python -m compas_rhino.install -p compas compas_rhino compas_ghpython compas_fab
