import os

from compas_viewer import Viewer

import compas
from compas.colors import Color
from compas.geometry import Line, Polygon

HERE = os.path.dirname(__file__)
cell_network = compas.json_load(os.path.join(HERE, "basics.datastructures.cell_networks.json"))

"""
viewer = Viewer()
for face in cell_network.faces():
    viewer.scene.add(Polygon(cell_network.face_coordinates(face)), facecolor=Color.silver())
for edge in cell_network.edges_without_face():
    line = Line(*cell_network.edge_coordinates(edge))
    viewer.scene.add(line, linewidth=3)
viewer.show()
"""


viewer = Viewer(show_grid=False)
no_cell = cell_network.faces_without_cell()
for face in cell_network.faces():
    if cell_network.is_face_on_boundary(face) is True:
        color = Color.silver()
        opacity = 0.5
    elif face in no_cell:
        color = Color.azure()
        opacity = 0.3
    else:
        color = Color.yellow()
        opacity = 0.8
    viewer.scene.add(Polygon(cell_network.face_coordinates(face)), facecolor=color, opacity=opacity)
for edge in cell_network.edges_without_face():
    line = Line(*cell_network.edge_coordinates(edge))
    viewer.scene.add(line, linewidth=3)
viewer.show()

