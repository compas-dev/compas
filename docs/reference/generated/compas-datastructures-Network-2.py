import compas
from compas.datastructures import Network
from compas.visualization import NetworkPlotter

network = Network.from_obj(compas.get_data('lines.obj'))

plotter = NetworkPlotter(network)

plotter.draw_vertices(text={key: key for key in network.vertices()}, radius=0.2)
plotter.draw_edges()

plotter.show()