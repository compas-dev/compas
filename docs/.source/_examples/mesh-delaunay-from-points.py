"""Delaunay triangulation from points"""

import compas_rhino as rhino

from compas.datastructures.mesh import Mesh
from compas.datastructures.mesh.algorithms import delaunay_from_points


__author__    = ['Tom Van Mele', 'Matthias Rippmann']
__copyright__ = 'Copyright 2017, BRG - ETH Zurich',
__license__   = 'MIT'
__email__     = 'van.mele@arch.ethz.ch'


guids = rhino.select_points()
vertices = rhino.get_point_coordinates(guids)

faces = delaunay_from_points(vertices)

mesh = Mesh.from_vertices_and_faces(vertices, faces)

rhino.draw_mesh(mesh)
