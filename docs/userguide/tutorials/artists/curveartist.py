from compas.geometry import NurbsCurve
from compas.artists import Artist

Artist.clear()

curve = NurbsCurve.from_points([[0, 0, 0], [3, 3, 6], [6, -3, -3], [9, 0, 0]])

artist = Artist(curve)
artist.color = (0.0, 1.0, 0.0)
artist.draw()

Artist.redraw()
