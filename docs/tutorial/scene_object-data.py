from compas.geometry import Point, Box, Frame

import compas_rhino
from compas_rhino.scene import Scene

compas_rhino.clear()

scene = Scene()

box = Box(Frame.worldXY(), 1, 1, 1)
obj = scene.add(box)

obj.item.frame.point = Point(3, 0, 0)
obj.draw()

scene.update()
