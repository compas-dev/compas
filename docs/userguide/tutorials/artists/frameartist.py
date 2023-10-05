from compas.geometry import Frame
from compas.artists import Artist

Artist.clear()

frame = Frame.worldXY()
artist = Artist(frame)
artist.draw()

Artist.redraw()
