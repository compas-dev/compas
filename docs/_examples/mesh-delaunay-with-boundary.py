"""Delaunay triangulation with boundary.

author : Matthias Rippmann
email  : rippmann@arch.ethz.ch

"""

import compas_rhino

from compas.datastructures import Mesh
from compas.geometry import delaunay_from_points

from compas_rhino.artists import MeshArtist


# select the points
# select the boundary
# select the hole(s)

guids = compas_rhino.select_points("Select points.")
points = compas_rhino.get_point_coordinates(guids)

guid = compas_rhino.select_polyline("Select boundary.")
boundary = compas_rhino.get_polyline_coordinates(guid)

guids = compas_rhino.select_polylines("Select holes.")
holes = [compas_rhino.get_polyline_coordinates(guid) for guid in guids]


# make a delaunay triangulation
# within the boundary
# and around the holes

faces = delaunay_from_points(points, boundary=boundary, holes=holes)
mesh = Mesh.from_vertices_and_faces(points, faces)


# draw the result

artist = MeshArtist(mesh)
artist.draw_faces(join_faces=True)
artist.redraw()
