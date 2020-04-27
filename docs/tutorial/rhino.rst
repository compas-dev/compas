********************************************************************************
Working in Rhino
********************************************************************************

To install COMPAS for Rhino, follow the "Getting Started" instructions provided here: :ref:`cad_rhino`.

Most of the core functionality of COMPAS (:mod:`compas`) is compatible with the IronPython interpreter in Rhino.
Therefore it can be embedded in scripts that can be executed with the `RunPythonScript` command.
Or it can be used in scripts in the

.. code-block:: python

    import compas
    from compas.datastructure import Mesh

    mesh = Mesh.from_off()

Functionality for processing Rhino Geometry, and visualisation of COMPAS objects (shapes, primitives, data structures)
is provided by :mod:`compas_rhino`.


Rhino Geometry
==============

:mod:`compas_rhino.geometry` provides several classes that simplify conversion
between Rhino objects and their COMPAS equivalents.

.. code-block:: python

    # pass


Artists
=======

.. note::

    Direct use of artists will soon be deprecated in favour of using Rhino scene objects.
    The goal of the scene objects is to further uniformise the use of COMPAS in CAD environments
    or in other visual/geometric interfaces such as the browser.

.. code-block:: python

    # pass


Remote Procedure Calls
======================

The Python interpreter in Rhino6 is an embedded version of IronPython 2.7.8.
This has both advatages and disadvantages.
The main advantage is that in addition to all built-in Python packages,
you have access to the DotNet platform.

.. code-block::

    import System
    import System.Net
    import System.IO
    import System.Drawing
    import System.Windows.Forms
    ...

The main disadvantage is that you do not have access to many of the interesting
scientific packages that are available for CPython.
The following (unfortunately) DOES NOT work.

.. code-block::

    import numpy
    import scipy
    import pandas
    import networkx
    import shapely
    import numba
    import sklearn
    ...

Therefore, in the core libraries of COMPAS we have taken great
care to separate functionality that CAN be imported from
functionality that CANNOT.

This difference is typically indicated through a backend suffix in the function name.
For example, the following algorithm is not directly available, as indicated by the ``_numpy`` suffix.

.. code-block:: python

    from compas.geometry import
