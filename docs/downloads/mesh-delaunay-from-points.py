"""Delaunay triangulation from points"""

import compas_rhino

from compas.datastructures import Mesh
from compas.datastructures import delaunay_from_points


__author__    = ['Tom Van Mele', 'Matthias Rippmann']
__copyright__ = 'Copyright 2017, BRG - ETH Zurich',
__license__   = 'MIT'
__email__     = 'van.mele@arch.ethz.ch'


guids = compas_rhino.select_points()
vertices = compas_rhino.get_point_coordinates(guids)

faces = delaunay_from_points(vertices)

mesh = Mesh.from_vertices_and_faces(vertices, faces)

compas_rhino.mesh_draw(mesh)
