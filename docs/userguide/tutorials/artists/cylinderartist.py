from compas.geometry import Cylinder
from compas.artists import Artist

Artist.clear()

cylinder = Cylinder(radius=1.0, height=7.0)

artist = Artist(cylinder)
artist.draw(color=(1.0, 0.0, 0.0))

Artist.redraw()
