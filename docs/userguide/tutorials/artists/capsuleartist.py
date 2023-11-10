from compas.geometry import Capsule
from compas.scene import SceneObject

SceneObject.clear()

capsule = Capsule(radius=1.0, height=7.0)

artist = SceneObject(capsule)
artist.draw(color=(1.0, 0.0, 0.0))

SceneObject.redraw()
