from compas.artists import Artist
from compas.geometry import Sphere

sphere = Sphere([0, 0, 0], 1)

Artist(sphere, u=32, v=32).draw()
