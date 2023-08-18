from random import randrange
from compas.geometry import Polyline
from compas.artists import Artist
from compas.colors import Color

Artist.clear()

polyline = Polyline([[0, 0, 0]])

for i, r in enumerate([randrange(1, 20) for _ in range(10)]):
    if i % 2 == 0:
        polyline.append([r, polyline.points[-1].y, 0])
    else:
        polyline.append([polyline.points[-1].x, r, 0])

artist = Artist(polyline)
artist.color = (0.0, 0.0, 1.0)
artist.draw()

Artist.redraw()
