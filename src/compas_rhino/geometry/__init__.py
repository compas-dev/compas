"""
This package provides plugins for various geometry pluggables using Rhino as the backend.
"""
# ruff: noqa: F401

from .curves.nurbs import RhinoNurbsCurve
from .surfaces.nurbs import RhinoNurbsSurface

from .brep.brep import RhinoBrep
from .brep.loop import RhinoBrepLoop
from .brep.vertex import RhinoBrepVertex
from .brep.face import RhinoBrepFace
from .brep.edge import RhinoBrepEdge
from .brep.trim import RhinoBrepTrim

from .booleans import boolean_difference_mesh_mesh
from .booleans import boolean_union_mesh_mesh
from .booleans import boolean_intersection_mesh_mesh

from .trimesh_curvature import trimesh_gaussian_curvature
from .trimesh_curvature import trimesh_mean_curvature
from .trimesh_curvature import trimesh_principal_curvature

from .trimesh_slicing import trimesh_slice
