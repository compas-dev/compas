**********
Extensions
**********

COMPAS provides many extensions that supplement the functionality of the core library,
and provide access to state-of-the-art research in the fields of
geometry processing, form finding, digital fabrication, discrete element modelling, finite element analysis, and many more.
Here, the extensions are listed that are managed by the core development team.
Extensions contributed by the community can be found at ...

.. figure:: /_images/COMPAS.png
     :figclass: figure
     :class: figure-img img-fluid


Core Extensions
===============

The core extension packages are COMPAS-friendly Python wrappers for libraries written in other languages, or for their Python bindings.
In many cases, the functionality of the extensions is implemented as plugins for the pluggable functions of COMPAS core.
It can be therefore be used from :mod:`compas` using the pluggables, or, of course, directly from the extension packages themselves.
A list of pluggables in COMPAS core is available here: :doc:`/devguide/pluggables`.

.. grid:: 1 1 2 2
    :gutter: 4

    .. grid-item-card:: compas_cgal
        :img-top: /_images/extensions/compas_cgal.png

        `compas_cgal <https://github.com/compas-dev/compas_cgal>`_ is a Python binding (generated with PyBind11) for a selection of algorithms of CGAL, The Computational Geometry Algorithms Library.
        Among other things, the package provides implementations for the pluggables for boolean operations, triangulation, remeshing, and mesh slicing.

    .. grid-item-card:: compas_gmsh
        :img-top: /_images/extensions/compas_gmsh.png

        `compas_gmsh <https://github.com/compas-dev/compas_gmsh>`_ is a wrapper for the Python binding of Gmsh, A three-dimensional finite element mesh generator with built-in pre- and post-processing facilities,
        and provides high quality 3D meshing functionality for Finite Element Analysis applications.

    .. grid-item-card:: compas_libigl
        :img-top: /_images/extensions/compas_libigl.png

        `compas_libigl <https://github.com/compas-dev/compas_libigl>`_ is a Python binding (generated with PyBind11) for a selection of algorithms of Libigl, the geometry processing library of the Interactive Geometry Lab.
        The package supplements the official Python binding of Libigl, and provides functionality that is easier to use in combination with COMPAS.

    .. grid-item-card:: compas_occ
        :img-top: /_images/extensions/compas_occ.png

        `compas_occ <https://github.com/compas-dev/compas_occ>`_ is a wrapper for the Python binding of OpenCascade
        and provides support for NURBS geometry and Boundary Representations (BREPs), independently of Rhino.

    .. grid-item-card:: compas_triangle
        :img-top: /_images/extensions/compas_triangle.png

        `compas_triangle <https://github.com/compas-dev/compas_triangle>`_ is a wrapper for the Cython implementation of Jonathan Shewchuck's Triangle library,
        a Two-Dimensional Quality Mesh Generator and Delaunay Triangulator.


CAD Interfaces
==============

COMPAS can be used in any environment that supports Python.
This means that it can be used in many CAD applications in combination with the CAD-specific Python scripting API, if available.
For some CAD applications, the core development team provides a dedicated extension package that provides a more specific bridge between COMPAS and the CAD application.

.. grid:: 1 1 2 2
    :gutter: 4

    .. grid-item-card:: compas_blender

        `compas_blender <https://github.com/compas-dev/compas_blender>`_ is a bridge between COMPAS and Blender.
        It provides functionality to convert between data structures in COMPAS and Blender,
        and to load and save geometry from and to files in the Blender format.

    .. grid-item-card:: compas_ghpython

        `compas_ghpython <https://github.com/compas-dev/compas_ghpython>`_ is a bridge between COMPAS and Blender.
        It provides functionality to convert between data structures in COMPAS and Blender,
        and to load and save geometry from and to files in the Blender format.

    .. grid-item-card:: compas_rhino

        `compas_rhino <https://github.com/compas-dev/compas_rhino>`_ is a bridge between COMPAS and Blender.
        It provides functionality to convert between data structures in COMPAS and Blender,
        and to load and save geometry from and to files in the Blender format.


AEC Tools
=========

.. grid:: 1 1 2 2
    :gutter: 4

    .. grid-item-card:: compas_fab
        :img-top: /_images/extensions/compas_fab.png

        Robotic fabrication package facilitating the planning and execution of robotic fabrication processes.
        It provides interfaces to existing software libraries and tools available in the field of robotics (e.g. OMPL, ROS)
        and makes them accessible from within the parametric design environment.

        `compas_fab <https://github.com/compas-dev/compas_fab>`_

    .. grid-item-card:: compas_fea
        :img-top: /_images/extensions/compas_fea.png

        Finite Element Analysis package providing an easy-to-use modelling language for FEA problems,
        and the possibility to use different backend solvers from a single problem description.

        `compas_fea <https://github.com/compas-dev/compas_fea2>`_

    .. grid-item-card:: compas_fofin

        Add description...

        `compas_fofin <https://github.com/compas-dev/compas_fofin>`_

    .. grid-item-card:: compas_ifc

        Add description...

        `compas_ifc <https://github.com/compas-dev/compas_ifc>`_

    .. grid-item-card:: compas_slicer
        :img-top: /_images/extensions/compas_slicer.png

        Add description...

        `compas_slicer <https://github.com/compas-dev/compas_slicer>`_

    .. grid-item-card:: compas_timber
        :img-top: /_images/extensions/compas_timber.png

        Add description...

        `compas_timber <https://github.com/compas-dev/compas_timber>`_

    .. grid-item-card:: compas_wood
        :img-top: /_images/extensions/compas_wood.png

        Add description...

        `compas_wood <https://github.com/compas-dev/compas_wood>`_
