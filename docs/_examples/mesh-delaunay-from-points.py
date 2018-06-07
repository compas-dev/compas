"""Delaunay triangulation from points"""

import compas_rhino

from compas.datastructures import Mesh
from compas.topology import delaunay_from_points

from compas_rhino.helpers import MeshArtist


__author__    = ['Tom Van Mele', 'Matthias Rippmann']
__copyright__ = 'Copyright 2017, BRG - ETH Zurich',
__license__   = 'MIT'
__email__     = 'van.mele@arch.ethz.ch'


# select the points
# and get their coordinates

guids = compas_rhino.select_points()
points = compas_rhino.get_point_coordinates(guids)


# make a mesh from the delaunay triangulation of the points

faces = delaunay_from_points(points)
mesh = Mesh.from_vertices_and_faces(points, faces)


# draw in Rhino

artist = MeshArtist(mesh)
artist.draw_faces(join_faces=True)
