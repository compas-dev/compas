# type: ignore

from compas_viewer import Viewer

from compas.colors import Color
from compas.datastructures import Mesh

mesh = Mesh.from_meshgrid(dx=9, nx=9)

viewer = Viewer(viewmode="top", width=1600, height=900)

red = Color.red()

viewer.scene.add(mesh, facecolor=(0.95, 0.95, 0.95), lineswidth=2)
viewer.scene.add(mesh.edge_line((30, 31)).translated([0, 0, 0.1]), linecolor=red, lineswidth=10)

for edge in mesh.edge_loop((30, 31)):
    viewer.scene.add(mesh.edge_line(edge).translated([0, 0, 0.1]), lineswidth=10)

viewer.show()
