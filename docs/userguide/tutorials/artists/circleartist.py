from compas.geometry import Circle
from compas.scene import SceneObject

SceneObject.clear()

circle = Circle(radius=3.0)

artist = SceneObject(circle)
artist.draw(color=(0.0, 0.0, 1.0), show_point=True, show_normal=True)

SceneObject.redraw()
