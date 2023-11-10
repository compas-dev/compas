from compas.geometry import Frame
from compas.scene import SceneObject

SceneObject.clear()

frame = Frame.worldXY()
artist = SceneObject(frame)
artist.draw()

SceneObject.redraw()
