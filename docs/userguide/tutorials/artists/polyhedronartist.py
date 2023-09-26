from compas.geometry import Polyhedron
from compas.artists import Artist

Artist.clear()

polyhedron = Polyhedron.from_platonicsolid(f=8)
artist = Artist(polyhedron)
artist.draw()

Artist.redraw()
