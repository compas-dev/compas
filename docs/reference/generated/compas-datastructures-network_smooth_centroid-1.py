import compas
from compas.datastructures.network import Network
from compas.visualization.plotters import NetworkPlotter
from compas.datastructures.network.algorithms import network_smooth_centroid

network  = Network.from_obj(compas.get_data('grid_irregular.obj'))

network_smooth_centroid(network, fixed=network.leaves(), kmax=10)

plotter = NetworkPlotter(network)

plotter.draw_vertices()
plotter.draw_edges()

plotter.show()