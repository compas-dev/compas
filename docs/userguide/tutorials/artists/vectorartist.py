from math import pi
from compas.geometry import Vector
from compas.geometry import Rotation
from compas.artists import Artist
from compas.colors import Color

Artist.clear()

vector = Vector(1, 0, 0)
artist = Artist(vector)
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

Artist.redraw()
