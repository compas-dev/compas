import compas
from compas.visualization.plotters import NetworkPlotter
from compas.datastructures import Network
network = Network.from_obj(compas.get_data('lines.obj'))
plotter = NetworkPlotter(network)
plotter.draw_vertices()
plotter.draw_edges()
plotter.show()