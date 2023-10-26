from compas.datastructures import Mesh
from compas.artists import Artist
from compas.colors import Color

mesh = Mesh.from_meshgrid(10, 10)

Artist.clear()

artist = Artist(mesh)
artist.draw_vertices()
artist.draw_edges()
artist.draw_faces(color={face: Color.pink() for face in mesh.face_sample(size=17)})
#artist.draw_vertexnormals()
artist.draw_facenormals()

Artist.redraw()
