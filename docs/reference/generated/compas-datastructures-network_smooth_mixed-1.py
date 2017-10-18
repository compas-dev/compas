import compas
from compas.datastructures import FaceNetwork
from compas.visualization import NetworkPlotter
from compas.datastructures import network_smooth_mixed
from compas.datastructures import network_find_faces

network = FaceNetwork.from_obj(compas.get_data('grid_irregular.obj'))
smooth = network.copy()

network_find_faces(smooth, breakpoints=smooth.leaves())

network_smooth_mixed(smooth,
                     [('centroid', 0.5), ('area', 0.5)],
                     fixed=smooth.leaves(),
                     kmax=10)

lines = []
for u, v, attr in network.edges(True):
    lines.append({
        'start': network.vertex_coordinates(u, 'xy'),
        'end'  : network.vertex_coordinates(v, 'xy'),
        'color': '#cccccc',
        'width': 1.0
    })

plotter = NetworkPlotter(smooth)

plotter.draw_xlines(lines)
plotter.draw_vertices(radius=0.15, text={key: key for key in smooth.vertices()})
plotter.draw_edges()

plotter.show()