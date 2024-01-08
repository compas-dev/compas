from compas.scene import Scene
from compas.geometry import Box
from compas.geometry import Capsule
from compas.geometry import Circle
from compas.geometry import Cone
from compas.geometry import Cylinder
from compas.geometry import Ellipse
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Polyhedron
from compas.geometry import Polyline
from compas.geometry import Sphere
from compas.geometry import Torus
from compas.geometry import Vector
# from compas.geometry import Plane

from compas.datastructures import Mesh
from compas.datastructures import Network
from compas.datastructures import VolMesh

from compas.geometry import Translation


box = Box.from_width_height_depth(1, 1, 1)
capsule = Capsule(0.5, 1, Frame.worldXY())
circle = Circle(1, Frame.worldXY())
cone = Cone(1, 1, Frame.worldXY())
cylinder = Cylinder(1, 1, Frame.worldXY())
line = Line(Point(0, 0, 0), Point(1, 1, 1))
point = Point(0, 0, 0)
polygon = Polygon.from_sides_and_radius_xy(5, 1)
polyhedron = Polyhedron.from_platonicsolid(4)
polyline = Polyline([[0, 0, 0], [1, 0, 0], [1, 0, 1]])
sphere = Sphere(1)
torus = Torus(1, 0.3, Frame.worldXY())
vector = Vector(0, 0, 1)

# TODO: Make these work everywhere
# ellipse = Ellipse(1, 0.5, Frame.worldXY())
# frame = Frame.worldXY()
# plane = Plane(Point(0, 0, 0), Vector(0, 0, 1))


mesh = Mesh.from_polyhedron(8)
network = Network.from_nodes_and_edges([(0, 0, 0), (0, -1.5, 0), (-1, 1, 0), (1, 1, 0)], [(0, 1), (0, 2), (0, 3)])
volmesh = VolMesh.from_meshgrid(1, 1, 1, 2, 2, 2)


scene = Scene()
scene.add(box)
scene.add(capsule)
scene.add(circle)
scene.add(cone)
scene.add(cylinder)
scene.add(line)
scene.add(point)
scene.add(polygon)
scene.add(polyhedron)
scene.add(polyline)
scene.add(sphere)
scene.add(torus)
scene.add(vector)

# scene.add(ellipse)
# scene.add(frame)
# scene.add(plane)

scene.add(mesh)
scene.add(network)
scene.add(volmesh)


x = 0
y = 0
for obj in scene.objects:
    obj.transformation = Translation.from_vector([x, y, 0])
    x += 5
    if x > 20:
        x = 0
        y += 5


scene.print_hierarchy()
scene.redraw()
