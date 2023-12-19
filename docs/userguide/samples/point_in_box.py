import math
from compas.geometry import Box, Pointcloud
from compas.colors import Color
from compas.scene import Scene

box = Box(2)
pcl = Pointcloud.from_bounds(x=10, y=10, z=5, n=1000)

box.rotate(math.radians(30))
box.translate(pcl.centroid)

scene = Scene()
scene.clear()

scene.add(box)

for point in pcl:
    color = Color.blue()
    size = 10
    if box.contains_point(point):
        color = Color.red()
        size = 30
    scene.add(point, pointcolor=color, pointsize=size)

scene.redraw()
