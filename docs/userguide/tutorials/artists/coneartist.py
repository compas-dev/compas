from compas.geometry import Cone
from compas.scene import SceneObject

SceneObject.clear()

cone = Cone(radius=1.0, height=7.0)

artist = SceneObject(cone)
artist.draw(color=(1.0, 0.0, 0.0))

SceneObject.redraw()
