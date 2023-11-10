from compas.geometry import Cylinder
from compas.scene import SceneObject

SceneObject.clear()

cylinder = Cylinder(radius=1.0, height=7.0)

artist = SceneObject(cylinder)
artist.draw(color=(1.0, 0.0, 0.0))

SceneObject.redraw()
