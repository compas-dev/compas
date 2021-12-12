from compas.artists import Artist
from compas.geometry import Box, Frame, Translation
from compas.datastructures import Mesh

box = Box(Frame.worldXY(), 1, 1, 1)
mesh = Mesh.from_shape(box)

mesh.transform(Translation.from_vector([2, 0, 0]))

artist = Artist(box)
artist.draw()

print(type(artist))

artist = Artist(mesh)
artist.draw()

print(type(artist))
