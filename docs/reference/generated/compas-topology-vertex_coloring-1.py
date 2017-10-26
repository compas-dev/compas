import compas
from compas.datastructures import Network
from compas.visualization import NetworkPlotter
from compas.topology import vertex_coloring

network = Network.from_obj(compas.get_data('grid_irregular.obj'))

key_color = vertex_coloring(network)
colors = ['#ff0000', '#00ff00', '#0000ff']

plotter = NetworkPlotter(network)

plotter.draw_vertices(facecolor={key: colors[key_color[key]] for key in network.vertices()})
plotter.draw_edges()

plotter.show()