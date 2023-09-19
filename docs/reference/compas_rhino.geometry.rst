********************************************************************************
compas_rhino.geometry
********************************************************************************

.. currentmodule:: compas_rhino.geometry

Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    RhinoCurve
    RhinoNurbsCurve
    RhinoNurbsSurface

    RhinoBrep
    RhinoBrepVertex
    RhinoBrepEdge
    RhinoBrepFace
    RhinoBrepLoop
    RhinoBrepTrim

Plugins
=======

Booleans
--------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    booleans.boolean_difference_mesh_mesh
    booleans.boolean_intersection_mesh_mesh
    booleans.boolean_union_mesh_mesh

Curves
------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    curves.new_curve
    curves.new_nurbscurve
    curves.new_nurbscurve_from_interpolation
    curves.new_nurbscurve_from_parameters
    curves.new_nurbscurve_from_points
    curves.new_nurbscurve_from_step

TriMesh
-------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    trimesh.trimesh_gaussian_curvature
    trimesh.trimesh_mean_curvature
    trimesh.trimesh_principal_curvature
    trimesh.trimesh_slice
