from compas.robots import Joint
from compas.robots import RobotModel
from compas.geometry import Box
from compas.geometry import Circle
from compas.geometry import Cylinder
from compas.geometry import Frame
from compas.geometry import Plane
from compas.geometry import Sphere
from compas.geometry import Vector

model = RobotModel('drinking_bird')

foot_1 = Box(Frame([2, .5, .25], [1, 0, 0], [0, 1, 0]), 1, 2, .5)
foot_2 = Box(Frame([-2, .5, .25], [1, 0, 0], [0, 1, 0]), 1, 2, .5)
leg_1 = Box(Frame([2, 0, 4], [1, 0, 0], [0, 1, 0]), .5, 1, 7)
leg_2 = Box(Frame([-2, 0, 4], [1, 0, 0], [0, 1, 0]), .5, 1, 7)
axis = Cylinder(Circle(Plane([0, 0, 7], [1, 0, 0]), .01), 4)
legs_link = model.add_link('legs', visual_meshes=[foot_1, foot_2, leg_1, leg_2, axis])

torso = Cylinder(Circle(Plane([0, 0, 0], [0, 0, 1]), .5), 8)
torso_link = model.add_link('torso', visual_meshes=[torso])

legs_joint_origin = Frame([0, 0, 7], [1, 0, 0], [0, 1, 0])
joint_axis = Vector(1, 0, 0)
model.add_joint(
    'torso_base_joint',
    Joint.CONTINUOUS,
    legs_link,
    torso_link,
    legs_joint_origin,
    joint_axis
)

head = Sphere([0, 0, 0], 1)
beak = Cylinder(Circle(Plane([0, 1, -.3], [0, 1, 0]), .3), 1.5)
head_link = model.add_link('head', visual_meshes=[head, beak])
neck_joint_origin = Frame([0, 0, 4], [1, 0, 0], [0, 1, 0])
model.add_joint('neck_joint', Joint.FIXED, torso_link, head_link, origin=neck_joint_origin)

tail = Sphere([0, 0, 0], 1)
tail_link = model.add_link('tail', visual_meshes=[tail])
tail_joint_origin = Frame([0, 0, -4], [1, 0, 0], [0, 1, 0])
model.add_joint('tail_joint', Joint.FIXED, torso_link, tail_link, origin=tail_joint_origin)

hat = Cylinder(Circle(Plane([0, 0, 0], [0, 0, 1]), .8), 1.5)
brim = Cylinder(Circle(Plane([0, 0, -1.5/2], [0, 0, 1]), 1.4), .1)
hat_link = model.add_link('hat', visual_meshes=[hat, brim])
hat_joint_origin = Frame([0, 0, 1 - .3 + 1.5/2], [1, 0, 0], [0, 1, 0])
model.add_joint('hat_joint', Joint.FIXED, head_link, hat_link, origin=hat_joint_origin)
