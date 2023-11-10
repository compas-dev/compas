from compas.geometry import Sphere
from compas.scene import SceneObject

SceneObject.clear()

sphere = Sphere(radius=1.0)

artist = SceneObject(sphere)
artist.draw(color=(1.0, 0.0, 0.0))

SceneObject.redraw()
