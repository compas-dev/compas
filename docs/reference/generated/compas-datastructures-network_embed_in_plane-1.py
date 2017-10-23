import compas

from compas.datastructures import Network
from compas.datastructures import network_embed_in_plane
from compas.visualization import NetworkPlotter

network = Network.from_obj(compas.get_data('fink.obj'))

embedding = network.copy()

fix = (1, 12)

if network_embed_in_plane(embedding, fix=fix):

    plotter = NetworkPlotter(embedding)

    plotter.draw_lines([{'start': network.vertex_coordinates(u, 'xy'),
                          'end': network.vertex_coordinates(v, 'xy'),
                          'color': '#cccccc'} for u, v in network.edges()])

    plotter.draw_vertices(radius=0.3,
                          text={key: key for key in embedding.vertices()},
                          facecolor={key: '#ff0000' for key in fix})

    plotter.draw_edges()
    plotter.show()