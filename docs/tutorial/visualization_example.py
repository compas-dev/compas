from compas.artists import Artist
from compas.geometry import Frame, Box

box = Box(Frame.worldXY(), 1, 1, 1)

Artist.clear()

Artist(box).draw(color=(255, 0, 0))

Artist.redraw()
