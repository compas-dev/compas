from math import radians

from compas_viewer import Viewer

from compas.colors import Color
from compas.geometry import Box
from compas.geometry import Pointcloud
from compas.geometry import Rotation
from compas.geometry import oriented_bounding_box

cloud = Pointcloud.from_bounds(10, 5, 3, 100)

Rz = Rotation.from_axis_and_angle([0.0, 0.0, 1.0], radians(60))
Ry = Rotation.from_axis_and_angle([0.0, 1.0, 0.0], radians(20))
Rx = Rotation.from_axis_and_angle([1.0, 0.0, 0.0], radians(10))

cloud.transform(Rz * Ry * Rx)

bbox = oriented_bounding_box(cloud)
box = Box.from_bounding_box(bbox)

viewer = Viewer()
viewer.scene.add(cloud)
viewer.scene.add(box, show_faces=False, linecolor=Color(1, 0, 0), linewidth=3)
viewer.show()
