import os

from compas_viewer import Viewer

import compas
from compas.colors import Color
from compas.datastructures import CellNetwork
from compas.geometry import Line, Polygon

cell_network = CellNetwork.from_json(compas.get("cellnetwork_example.json"))


viewer = Viewer(show_grid=False)
no_cell = cell_network.faces_without_cell()
for face in cell_network.faces():
    if cell_network.is_face_on_boundary(face) is True:
        color, opacity = Color.silver(), 0.5
    elif face in no_cell:
        color, opacity = Color.azure(), 0.3
    else:
        color, opacity = Color.yellow(), 0.8
    viewer.scene.add(Polygon(cell_network.face_coordinates(face)), facecolor=color, opacity=opacity)
for edge in cell_network.edges_without_face():
    line = Line(*cell_network.edge_coordinates(edge))
    viewer.scene.add(line, linewidth=3)

graph = cell_network.cells_to_graph()
viewer.scene.add(graph)

viewer.show()