from math import radians

import compas
import compas_rhino

from compas.geometry import rotate_points

from compas.datastructures import Mesh

from compas_rhino.artists import MeshArtist

# make a mesh from the Stanford bunny PLY file

mesh = Mesh.from_ply(compas.get_bunny())

# rotate the bunny to align it with the Z axis
# display the results in Rhino

points = [mesh.vertex_coordinates(key) for key in mesh.vertices()]
points = rotate_points(points, radians(90), [1.0, 0.0, 0.0])

for index, (key, attr) in enumerate(mesh.vertices(True)):
    attr['x'] = points[index][0]
    attr['y'] = points[index][1]
    attr['z'] = points[index][2]


artist = MeshArtist(mesh)
artist.draw_faces(join_faces=True)
artist.redraw()
