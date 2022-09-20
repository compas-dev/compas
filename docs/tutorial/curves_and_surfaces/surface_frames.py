from compas.geometry import Point
from compas.utilities import meshgrid, flatten
from compas.geometry import NurbsSurface
from compas.artists import Artist


points = [
    [Point(0, 0, 0), Point(1, 0, 0), Point(2, 0, 0), Point(3, 0, 0)],
    [Point(0, 1, 0), Point(1, 1, 2), Point(2, 1, 2), Point(3, 1, 0)],
    [Point(0, 2, 0), Point(1, 2, 2), Point(2, 2, 2), Point(3, 2, 0)],
    [Point(0, 3, 0), Point(1, 3, 0), Point(2, 3, 0), Point(3, 3, 0)],
]

surface = NurbsSurface.from_points(points=points)

# ==============================================================================
# Frames
# ==============================================================================

U, V = meshgrid(surface.u_space(), surface.v_space(), "ij")
frames = [surface.frame_at(u, v) for u, v in zip(flatten(U), flatten(V))]

# ==============================================================================
# Visualisation
# ==============================================================================

Artist.clear()

Artist(surface).draw()

for frame in frames:
    Artist(frame).draw()

Artist.redraw()
