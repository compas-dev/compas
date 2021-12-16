from compas.geometry import Frame, Box
from compas_rhino.artists import BoxArtist

box = Box(Frame.worldXY(), 1, 1, 1)

artist = BoxArtist(box)
artist.draw()
