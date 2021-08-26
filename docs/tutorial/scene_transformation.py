from __future__ import print_function

from compas.geometry import Box, Frame, Translation

import compas_rhino
from compas_rhino.scene import Scene

compas_rhino.clear()

scene = Scene()

box = Box(Frame.worldXY(), 1, 1, 1)
obj = scene.add(box)

obj.transform(Translation.from_vector([3, 0, 0]))

print(obj.item.frame.point)
print(box.frame.point)

obj.synchronize()

print(obj.item.frame.point)
print(box.frame.point)

scene.update(pause=1)
