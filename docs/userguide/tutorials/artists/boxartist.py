from compas.geometry import Box
from compas.scene import SceneObject

SceneObject.clear()

box = Box.from_corner_corner_height([0, 0, 0], [1, 1, 0], 3)

artist = SceneObject(box, layer='Test::Child')
artist.draw(color=(0.0, 1.0, 0.0))

SceneObject.redraw()
