***************
Core Extensions
***************

.. warning::

    This page is still under construction.
    Therefore its contents are likely to change frequently...

The core extension packages are COMPAS-friendly Python wrappers for libraries written in other languages, or for their Python bindings.
In many cases, the functionality of the extensions is implemented as plugins for the pluggable functions of COMPAS core.
It can be therefore be used from :mod:`compas` using the pluggables, or, of course, directly from the extension packages themselves.
A list of pluggables in COMPAS core is available here: :doc:`/devguide/pluggables`.

compas_cgal
===========

`compas_cgal <https://github.com/compas-dev/compas_cgal>`_ is a Python binding (generated with PyBind11) for a selection of algorithms of `CGAL, The Computational Geometry Algorithms Library <https://www.cgal.org/>`_.
Among other things, the package provides implementations for the pluggables for boolean operations, triangulation, remeshing, and mesh slicing.

.. code-block:: python

    # this snippet should be updated...

    from compas.geometry import Box, Sphere

    A = Box(2, 2, 2)
    B = Sphere(1, point=[1, 1, 1])

    C = A + B

compas_occ
==========

`compas_occ <https://github.com/compas-dev/compas_occ>`_ is a wrapper for the Python binding (:mod:`pythonocc`) of `OpenCascade <https://www.opencascade.com/open-cascade-technology/>`_.
and provides support for NURBS geometry and Boundary Representations (BREPs), independently of Rhino.

.. code-block:: python

    from compas.geometry import Point, NurbsSurface

    points = [
        [Point(0, 0, 0), Point(1, 0, 0), Point(2, 0, 0), Point(3, 0, 0)],
        [Point(0, 1, 0), Point(1, 1, 2), Point(2, 1, 2), Point(3, 1, 0)],
        [Point(0, 2, 0), Point(1, 2, 2), Point(2, 2, 2), Point(3, 2, 0)],
        [Point(0, 3, 0), Point(1, 3, 0), Point(2, 3, 0), Point(3, 3, 0)],
    ]

    surface = NurbsSurface.from_points(points)

compas_libigl
=============

`compas_libigl <https://github.com/compas-dev/compas_libigl>`_ is a Python binding (generated with PyBind11) for a selection of algorithms of `libigl, the geometry processing library of the Interactive Geometry Lab <https://libigl.github.io>`_.
The package supplements the `official Python binding of libigl <https://anaconda.org/conda-forge/igl>`_, and provides functionality that is easier to use in combination with COMPAS.

.. code-block:: python

    # add snippet...

compas_gmsh
===========

`compas_gmsh <https://github.com/compas-dev/compas_gmsh>`_ is a wrapper for the Python binding (:mod:`gmsh`) of `Gmsh, A three-dimensional finite element mesh generator with built-in pre- and post-processing facilities <https://gmsh.info/>`_,
and provides high quality 3D meshing functionality for Finite Element Analysis applications.

.. code-block:: python

    # add snippet...

compas_triangle
===============

`compas_triangle <https://github.com/compas-dev/compas_triangle>`_ is a wrapper for the
`Cython implementation <https://github.com/drufat/triangle>`_ of Jonathan Shewchuck's `Triangle <https://www.cs.cmu.edu/~quake/triangle.html>`_ library,
a Two-Dimensional Quality Mesh Generator and Delaunay Triangulator.

.. code-block:: python

    # add snippet...
