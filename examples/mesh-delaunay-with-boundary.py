"""Delaunay triangulation with boundary"""

from compas.datastructures import Mesh
from compas.datastructures import delaunay_from_points

import compas_rhino


__author__    = ['Tom Van Mele', 'Matthias Rippmann']
__copyright__ = 'Copyright 2017, BRG - ETH Zurich',
__license__   = 'MIT'
__email__     = 'van.mele@arch.ethz.ch'


guids = compas_rhino.select_points()
vertices = compas_rhino.get_point_coordinates(guids)

guid = compas_rhino.select_polyline("Select boundary.")
boundary = compas_rhino.get_polyline_coordinates(guid)

guids = compas_rhino.select_polylines("Select holes.")
holes = [compas_rhino.get_polyline_coordinates(guid) for guid in guids]

faces = delaunay_from_points(vertices, boundary, holes)

mesh = Mesh.from_vertices_and_faces(vertices, faces)

compas_rhino.mesh_draw(mesh)
