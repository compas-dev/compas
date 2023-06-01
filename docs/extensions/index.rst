**********
Extensions
**********

Core Extensions
===============

The core extension packages are Python wrappers for libraries written in other languages,
or for their Python bindings,
and define many of the plugins for the pluggables of the core library.
They can of course also be used independently as normal Python packages.

:mod:`compas_occ`
-----------------

:mod:`compas_occ` is a wrapper for the Python binding (:mod:`pythonocc`) of `OpenCascade <https://www.opencascade.com/open-cascade-technology/>`_.
and provides support for NURBS geometry and Boundary Representations (BREPs), independently of Rhino.

Most of the functionality of the package can be used from :mod:`compas.geometry` through the plugin system
in any environment where :mod:`compas` and :mod:`compas_occ` are both installed.

.. code-block:: python

    from compas.geometry import Point, NurbsSurface


    points = [
        [Point(0, 0, 0), Point(1, 0, 0), Point(2, 0, 0), Point(3, 0, 0)],
        [Point(0, 1, 0), Point(1, 1, 2), Point(2, 1, 2), Point(3, 1, 0)],
        [Point(0, 2, 0), Point(1, 2, 2), Point(2, 2, 2), Point(3, 2, 0)],
        [Point(0, 3, 0), Point(1, 3, 0), Point(2, 3, 0), Point(3, 3, 0)],
    ]

    surface = NurbsSurface.from_points(points=points)


For more information, see `compas_occ <https://github.com/compas-dev/compas_occ>`_

:mod:`compas_cgal`
------------------

:mod:`compas_cgal` is a Python binding (generated with PyBind11) for a selection of algorithms of
`CGAL <https://www.cgal.org/>`_, The Computational Geometry Algorithms Library.

The functionality of the package is available in :mod:`compas.geometry` through the plugin system, or, of course, from :mod:`compas_cgal` directly.

.. code-block:: python

    # add snippet

For more information, see `compas_cgal <https://github.com/compas-dev/compas_cgal>`_

AEC Extensions
==============

.. grid::

    .. grid-item-card:: :mod:`compas_occ`

        Wrapper for the Python binding (:mod:`pythonocc`) of OpenCascade.
        Provides support for NURBS geometry and Boundary Representations (BREPs), independently of Rhino.

        `compas_occ <https://github.com/compas-dev/compas_occ>`_

    .. grid-item-card:: :mod:`compas_cgal`

        Wrapper for specific algorithms of CGAL, the Computational Geometry Algorithms Library.
        Among other things, provides support for boolean operations on triangle meshes.

        `compas_cgal <https://github.com/compas-dev/compas_cgal>`_

Other Extensions
================

For an overview of extension packages developed by the community, see ...
