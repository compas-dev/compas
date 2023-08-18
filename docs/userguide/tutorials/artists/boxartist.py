from compas.geometry import Box
from compas.artists import Artist

Artist.clear()

box = Box.from_corner_corner_height([0, 0, 0], [1, 1, 0], 3)

artist = Artist(box)
artist.draw(color=(0.0, 1.0, 0.0))


Artist.redraw()