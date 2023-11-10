from compas.datastructures import Mesh
from compas.scene import SceneObject
from compas.colors import Color

mesh = Mesh.from_meshgrid(10, 10)

SceneObject.clear()

artist = SceneObject(mesh)
artist.draw_vertices()
artist.draw_edges()
artist.draw_faces(color={face: Color.pink() for face in mesh.face_sample(size=17)})
#artist.draw_vertexnormals()
artist.draw_facenormals()

SceneObject.redraw()
