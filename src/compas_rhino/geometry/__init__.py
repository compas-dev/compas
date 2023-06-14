"""
********************************************************************************
geometry
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

"""
from __future__ import absolute_import

from compas_rhino.conversions import RhinoGeometry

from compas_rhino.conversions import RhinoBox
from compas_rhino.conversions import RhinoCircle
from compas_rhino.conversions import RhinoCone
from compas_rhino.conversions import RhinoCurve
from compas_rhino.conversions import RhinoCylinder
from compas_rhino.conversions import RhinoEllipse
from compas_rhino.conversions import RhinoLine
from compas_rhino.conversions import RhinoMesh
from compas_rhino.conversions import RhinoPlane
from compas_rhino.conversions import RhinoPoint
from compas_rhino.conversions import RhinoPolyline
from compas_rhino.conversions import RhinoSphere
from compas_rhino.conversions import RhinoSurface
from compas_rhino.conversions import RhinoVector

from .curves import RhinoNurbsCurve
from .surfaces import RhinoNurbsSurface

from .brep import RhinoBrep
from .brep import RhinoBrepLoop
from .brep import RhinoBrepVertex
from .brep import RhinoBrepFace
from .brep import RhinoBrepEdge
from .brep import RhinoBrepTrim

__all__ = [
    "RhinoGeometry",
    "RhinoBox",
    "RhinoCircle",
    "RhinoCone",
    "RhinoCurve",
    "RhinoCylinder",
    "RhinoEllipse",
    "RhinoLine",
    "RhinoMesh",
    "RhinoPlane",
    "RhinoPoint",
    "RhinoPolyline",
    "RhinoSphere",
    "RhinoSurface",
    "RhinoVector",
    "RhinoNurbsCurve",
    "RhinoNurbsSurface",
    "RhinoBrep",
    "RhinoBrepVertex",
    "RhinoBrepEdge",
    "RhinoBrepFace",
    "RhinoBrepLoop",
    "RhinoBrepTrim",
]
