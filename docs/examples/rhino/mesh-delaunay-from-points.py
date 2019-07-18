import compas_rhino

from compas.datastructures import Mesh
from compas.topology import delaunay_from_points

from compas_rhino.artists import MeshArtist

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
artist.redraw()
