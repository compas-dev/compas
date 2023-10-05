import compas_rhino

from compas.geometry import Point
from compas.artists import Artist
from compas.colors import Color

compas_rhino.clear()

point = Point(0, 0, 0)
artist = Artist(point)
# artist.color = (0.0, 1.0, 0.0)

for i in range(11):
    point.x = i
    artist.draw(color=Color.from_i(i / 10))

compas_rhino.redraw()
