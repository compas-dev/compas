import random
from compas.geometry import Polyline
from compas.geometry import NurbsSurface
from compas.artists import Artist


U = 10
V = 20

surface = NurbsSurface.from_meshgrid(nu=U, nv=V)

# ==============================================================================
# Update
# ==============================================================================

for u in range(1, U):
    for v in range(1, V):
        point = surface.points[u, v]
        point.z = random.choice([+1, -1]) * random.random()
        surface.points[u, v] = point

# ==============================================================================
# Visualisation
# ==============================================================================

Artist.clear()

for row in surface.points:
    Artist(Polyline(row)).draw()

for col in zip(*list(surface.points)):
    Artist(Polyline(col)).draw()

Artist(surface).draw()

Artist.redraw()
