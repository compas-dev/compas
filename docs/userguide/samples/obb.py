from math import radians

from compas.geometry import Pointcloud, Box
from compas.geometry import Rotation
from compas.geometry import oriented_bounding_box

from compas_view2.app import App

cloud = Pointcloud.from_bounds(10, 5, 3, 100)

Rz = Rotation.from_axis_and_angle([0.0, 0.0, 1.0], radians(60))
Ry = Rotation.from_axis_and_angle([0.0, 1.0, 0.0], radians(20))
Rx = Rotation.from_axis_and_angle([1.0, 0.0, 0.0], radians(10))

cloud.transform(Rz * Ry * Rx)

bbox = oriented_bounding_box(cloud)
box = Box.from_bounding_box(bbox)

viewer = App()
viewer.add(cloud)
viewer.add(box, show_faces=False, linecolor=(1, 0, 0), linewidth=3)
viewer.run()
