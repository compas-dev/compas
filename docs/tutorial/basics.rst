******
Basics
******

.. highlight:: python


By installing COMPAS (see :ref:`installation`), the following packages are installed:

* :mod:`compas`
* :mod:`compas_blender`
* :mod:`compas_ghpython`
* :mod:`compas_plotters`
* :mod:`compas_rhino`

The :mod:`compas` package provides the core functionality of the COMPAS framework.
The packages :mod:`compas_rhino`, :mod:`compas_ghpython`, and :mod:`compas_blender` provide integration in Rhino, Grasshopper (through GHPython) and Blender, respectively.
:mod:`compas_plotters` provides 2D visualization tools based on :mod:`matplotlib`.


Code structure
==============

In all packages, functionality is made available at the first sub-package level.

::

    >>> from compas.datastructures import Mesh
    >>> from compas.geometry import Point
    >>> from compas.numerical import dr_numpy


Core functionality
==================

The core functionality of the framework is written entirely in CPython such that it can easily be used across platform,
in various coding environments, and inside software tools the provide a Python scripting interface.

To speed up computation, some functionality is based on Numpy/Scipy.
These functions are suffixed with ``_numpy``.

Numpy/Scipy function variants are available in all environments except for Rhino and GHPython since Numpy and Scipy are not available for IronPython.
However, ``_numpy`` functions can be used in Rhino or Grasshopper through Remote Procedure Calls (:mod:`compas.rpc`)


Plugin functionality
====================

*PLACEHOLDER*


CAD integration
===============

:mod:`compas` can be used directly in any CAD software that provides support for Python scripting.
The CAD packages (:mod:`compas_rhino`, :mod:`compas_ghpython`, :mod:`compas_blender`)
provide specific support for visualizing COMPAS objects, for processing native CAD geometry,
and for building simple UIs, in Rhino, Grasshopper and Blender, respectively.
