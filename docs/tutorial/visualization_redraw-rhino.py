import time
from compas.geometry import Frame, Box, Translation
from compas.artists import Artist

box = Box(Frame.worldXY(), 1, 1, 1)

artist = Artist(box)
artist.draw()
Artist.redraw()

T = Translation.from_vector([1, 0, 0])

for i in range(10):
    time.sleep(1)
    box.transform(T)
    artist.draw()
    Artist.redraw()
