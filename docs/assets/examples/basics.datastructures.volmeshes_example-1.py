from math import radians

import numpy
from compas_viewer import Viewer
from compas_viewer.config import Config
from compas_viewer.scene import BufferGeometry

from compas.colors import Color
from compas.datastructures import VolMesh
from compas.geometry import Box
from compas.geometry import Plane
from compas.tolerance import Tolerance

tolerance = Tolerance()

# =============================================================================
# Base Box
# =============================================================================

box = Box(10).to_mesh()

# =============================================================================
# Cutting Planes
# =============================================================================

planes = [
    Plane.worldXY().rotated(radians(30), [0, 1, 0]),
    Plane.worldYZ().rotated(radians(30), [0, 0, 1]),
    Plane.worldZX().rotated(radians(30), [1, 0, 0]),
    Plane.worldXY().translated([0, 0, +2.5]),
    Plane.worldXY().translated([0, 0, -2.5]),
]

# =============================================================================
# Cuts
# =============================================================================

results = [box]
for plane in planes:
    temp = []
    for box in results:
        result = box.slice(plane)
        if result:
            temp += result
        else:
            temp.append(box)
    results = temp

# =============================================================================
# VolMesh Construction
# =============================================================================

volmesh = VolMesh.from_meshes(results)

volmesh.translate([5, 5, 5])

# =============================================================================
# Visualisation
# =============================================================================

config = Config()
config.camera.target = [5, 5, 5]
config.camera.position = [-8, -15, 10]

viewer = Viewer(config=config)

wires = numpy.asarray([volmesh.edge_coordinates(edge) for edge in volmesh.edges()])
viewer.scene.add(BufferGeometry(lines=wires), name="Wires")

cell = list(volmesh.cell_sample(size=1))[0]
cell_color = {cell: Color.red()}
for nbr in volmesh.cell_neighbors(cell):
    cell_color[nbr] = Color.green()

for cell in cell_color:
    color = cell_color[cell]
    mesh = volmesh.cell_to_mesh(cell)
    viewer.scene.add(mesh, facecolor=color)

viewer.show()
