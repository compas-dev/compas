import random
from math import radians

from compas.geometry import pointcloud
from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import Rotation
from compas.geometry import Translation
from compas.geometry import icp_numpy
from compas_plotters import Plotter2

R = Rotation.from_axis_and_angle(Vector.Zaxis(), radians(30))

source = [Point(*xyz) for xyz in pointcloud(30, (0, 10), (0, 5), (0, 3))]
observations = Point.transformed_collection(source, R)

noise = []
for i in range(5):
    point = random.choice(observations)
    T = Translation([random.random(), random.random(), random.random()])
    noise.append(point.transformed(T))

outliers = [Point(*xyz) for xyz in pointcloud(3, (10, 15), (0, 5), (0, 3))]
Point.transform_collection(outliers, R)

target = observations + noise + outliers

A, X = icp_numpy(source, target)

source_new = [Point(*point) for point in A]

plotter = Plotter2()
[plotter.add(point, facecolor=(1.0, 1.0, 1.0)) for point in source]
[plotter.add(point, facecolor=(0.0, 0.0, 0.0)) for point in target]
[plotter.add(point, facecolor=(1.0, 0.0, 0.0)) for point in source_new]
plotter.zoom_extents()
plotter.show()
