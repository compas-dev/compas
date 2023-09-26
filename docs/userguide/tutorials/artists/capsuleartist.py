from compas.geometry import Capsule
from compas.artists import Artist

Artist.clear()

capsule = Capsule(radius=1.0, height=7.0)

artist = Artist(capsule)
artist.draw(color=(1.0, 0.0, 0.0))

Artist.redraw()
