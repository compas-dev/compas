from compas.datastructures import Mesh
from compas.artists import Artist
from compas.colors import Color

mesh = Mesh.from_meshgrid(10, 10)

Artist.clear()

artist = Artist(mesh)
artist.draw_faces(color={face: Color.pink() for face in mesh.face_sample(size=17)})

Artist.redraw()
