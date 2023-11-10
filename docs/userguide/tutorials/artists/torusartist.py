from compas.geometry import Torus
from compas.scene import SceneObject

SceneObject.clear()

torus = Torus(radius_axis=7.0, radius_pipe=2.0)

artist = SceneObject(torus)
artist.draw(color=(1.0, 0.0, 0.0))

SceneObject.redraw()
