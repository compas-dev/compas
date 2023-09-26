from compas.geometry import Torus
from compas.artists import Artist

Artist.clear()

torus = Torus(radius_axis=7.0, radius_pipe=2.0)

artist = Artist(torus)
artist.draw(color=(1.0, 0.0, 0.0))

Artist.redraw()
