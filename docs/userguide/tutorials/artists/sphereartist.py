from compas.geometry import Sphere
from compas.artists import Artist

Artist.clear()

sphere = Sphere(radius=1.0)

artist = Artist(sphere)
artist.draw(color=(1.0, 0.0, 0.0))

Artist.redraw()
