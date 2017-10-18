import compas
from compas.datastructures import Network
from compas.datastructures import network_smooth_centroid
from compas.visualization import NetworkPlotter

network  = Network.from_obj(compas.get_data('grid_irregular.obj'))

network_smooth_centroid(network, fixed=network.leaves(), kmax=10)

plotter = NetworkPlotter(network)

plotter.draw_vertices()
plotter.draw_edges()

plotter.show()