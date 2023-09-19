from compas.geometry import Cone
from compas.artists import Artist

Artist.clear()

cone = Cone(radius=1.0, height=7.0)

artist = Artist(cone)
artist.draw(color=(1.0, 0.0, 0.0))

Artist.redraw()
