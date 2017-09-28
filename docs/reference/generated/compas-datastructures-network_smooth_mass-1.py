import compas
from compas.datastructures import FaceNetwork
from compas.visualization.plotters import NetworkPlotter
from compas.datastructures.network.algorithms import network_find_faces
from compas.datastructures.network.algorithms import network_smooth_mass

network = FaceNetwork.from_obj(compas.get_data('grid_irregular.obj'))

network_find_faces(network, network.leaves())
network_smooth_mass(network, fixed=network.leaves(), kmax=10)

plotter = NetworkPlotter(network)

plotter.draw_vertices()
plotter.draw_edges()

plotter.show()