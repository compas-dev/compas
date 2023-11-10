from math import pi
from compas.geometry import Vector
from compas.geometry import Rotation
from compas.scene import SceneObject
from compas.colors import Color

SceneObject.clear()

vector = Vector(1, 0, 0)
artist = SceneObject(vector)
# artist.color = (0.0, 1.0, 0.0)

# for i in range(11):
#     artist.draw(
#         color=Color.from_i(i / 10),
#         point=[i, 0, 0],
#         show_point=True
#     )

step = pi / 10.0

for i in range(11):
    artist.draw(color=Color.from_i(i / 10))

    rotation = Rotation.from_axis_and_angle([0, 0, 1], angle=step)
    vector.transform(rotation)

SceneObject.redraw()
