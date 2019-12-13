Basics
======

By installing COMPAS (see :ref:`Installation`), the following packages are installed:

* :mod:`compas`
* :mod:`compas_blender`
* :mod:`compas_ghpython`
* :mod:`compas_plotters`
* :mod:`compas_rhino`

The :mod:`compas` package provides the core functionality of the COMPAS framework.
The packages :mod:`compas_rhino`, :mod:`compas_ghpython`, and :mod:`compas_blender` provide integration in Rhino, Grasshopper (through GHPython) and Blender, respectively.
:mod:`compas_plotters` provides 2D visualization tools based on :mod:`matplotlib`.


Code structure
--------------

In all packages, functionality is made available at the first sub-package level.

.. code-block:: python

    from compas.datastructures import Mesh
    from compas.geometry import Point
    from compas.numerical import dr_numpy

.. code-block:: python

    # Rhino only

    from compas_rhino.artists import MeshArtist
    from compas_rhino.geometry import RhinoSurface

.. code-block:: python

    # Blender only

    from compas_blender.artists import MeshArtist


Core functionality
------------------

The core functionallity of the framework is written entirely in CPython such that it can easily be used across platform,
in various coding environments, and inside software tools the provide a Python scripting interface.

To speed up computation, some functionality is based on Numpy/Scipy.
These functions are suffixed with ``_numpy``.

They are available in all environments except for Rhino and GHPython since Numpy and Scipy are not available for IronPython.
``_numpy`` functions can be used in Rhino or Grasshopper through Remote Procedure Calls (:mod:`compas.rpc`)


CAD integration
---------------

:mod:`compas` can be used directly in CAD software that provides support for Python scripting.
The CAD packages (:mod:`compas_rhino`, :mod:`compas_ghpython`, :mod:`compas_blender`)
provide classes and functionality for visualizing COMPAS data structures and geometry,
for processing native CAD geometry, and for building simple UIs.

Visualization is handled by *Artists*.
An artist is available for every data structure, geometric primitive and shape.

.. code-block:: python

    from compas.datastructures import Mesh
    from compas_rhino.artists import MeshArtist

