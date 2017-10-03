import compas

from compas.datastructures import FaceNetwork
from compas.datastructures import network_find_faces
from compas.datastructures import network_dual
from compas.visualization.plotters import NetworkPlotter

network = FaceNetwork.from_obj(compas.get_data('grid_irregular.obj'))

network_find_faces(network, breakpoints=network.leaves())

dual = network_dual(network)

plotter = NetworkPlotter(dual)

lines = []
for u, v in network.edges():
    lines.append({
        'start': network.vertex_coordinates(u, 'xy'),
        'end': network.vertex_coordinates(v, 'xy'),
        'color': '#cccccc'
    })

points = []
for key in network.vertices():
    points.append({
        'pos': network.vertex_coordinates(key, 'xy'),
        'facecolor': '#ff0000',
        'edgecolor': '#000000',
        'radius': 0.075,
    })

plotter.draw_xlines(lines)
plotter.draw_xpoints(points)
plotter.draw_vertices(radius=0.15, facecolor='#ffffff', edgecolor='#444444', text={key: key for key in network.vertices()})
plotter.draw_edges()

plotter.show()