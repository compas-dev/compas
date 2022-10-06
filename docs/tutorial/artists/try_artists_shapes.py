import random
from compas.geometry import Box, Sphere, Cylinder, Cone, Capsule, Torus, Polyhedron
from compas.geometry import Plane, Circle, Pointcloud
from compas.geometry import Translation
from compas.artists import Artist
from compas.colors import Color

shapes = [
    Box.from_width_height_depth(1, 1, 1),
    Sphere([0, 0, 0], 0.3),
    Cylinder(Circle(Plane([0, 0, 0], [0, 0, 1]), 0.3), 1.0),
    Cone(Circle(Plane([0, 0, 0], [0, 0, 1]), 0.3), 1.0),
    Capsule([[0, 0, 0], [1, 0, 0]], 0.2),
    Torus(Plane([0, 0, 0], [0, 0, 1]), 1.0, 0.3),
    Polyhedron.from_platonicsolid(12),
]

cloud = Pointcloud.from_bounds(8, 5, 3, len(shapes))

Artist.clear()

for point, shape in zip(cloud, shapes):
    shape.transform(Translation.from_vector(point))
    artist = Artist(shape)
    artist.draw(color=Color.from_i(random.random()))

Artist.redraw()
