
********************************************************************************
compas_rhino.geometry
********************************************************************************

.. currentmodule:: compas_rhino.geometry

.. rst-class:: lead


This package provides plugins for various geometry pluggables using Rhino as the backend.


Classes
=======



.. autosummary::
    :toctree: generated/
    :nosignatures:

    RhinoBrep
    RhinoBrepEdge
    RhinoBrepFace
    RhinoBrepLoop
    RhinoBrepTrim
    RhinoBrepVertex
    RhinoNurbsCurve
    RhinoNurbsSurface


Plugins
=======

Plugins provide implementations for pluggables. You can use the plugin directly, or through the pluggable.

.. autosummary::
    :toctree: generated/
    :nosignatures:

    boolean_difference_mesh_mesh
    boolean_intersection_mesh_mesh
    boolean_union_mesh_mesh
    trimesh_gaussian_curvature
    trimesh_mean_curvature
    trimesh_principal_curvature
    trimesh_slice



