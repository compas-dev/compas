from compas.datastructures import Mesh
from compas.scene import SceneObject
from compas.colors import Color

mesh = Mesh.from_meshgrid(10, 10)

SceneObject.clear()

artist = SceneObject(mesh)
artist.draw_faces(color={face: Color.pink() for face in mesh.face_sample(size=17)})

SceneObject.redraw()
