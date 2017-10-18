import compas
from compas.datastructures import FaceNetwork
from compas.datastructures import network_find_faces
from compas.visualization import NetworkPlotter

network = FaceNetwork.from_obj(compas.get_data('lines.obj'))

network_find_faces(network, breakpoints=network.leaves())

plotter = NetworkPlotter(network, figsize=(10, 7))

plotter.defaults['vertex.fontsize'] = 8.0

plotter.draw_vertices(
    facecolor={key: '#ff0000' for key in network.leaves()},
    radius=0.2,
    text={key: key for key in network.vertices()}
)

plotter.draw_faces(facecolor='#eeeeee', edgecolor='#eeeeee')
plotter.draw_edges()

plotter.show()