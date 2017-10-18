import compas
from compas.datastructures import Network
from compas.visualization import NetworkPlotter
from compas.datastructures import network_embed_in_plane

network = Network.from_obj(compas.get_data('fink.obj'))
embedding = network.copy()

fix = (1, 12)

if network_embed_in_plane(embedding, fix=fix):

    plotter = NetworkPlotter(embedding)

    points = []
    for key in network.vertices():
        points.append({
            'pos': network.vertex_coordinates(key, 'xy'),
            'radius': 0.1
        })

    lines = []
    for u, v in network.edges():
        lines.append({
            'start': network.vertex_coordinates(u, 'xy'),
            'end'  : network.vertex_coordinates(v, 'xy'),
            'color': '#cccccc',
        })

    plotter.draw_xlines(lines)
    plotter.draw_xpoints(points)

    plotter.draw_edges()
    plotter.draw_vertices(facecolor={key: ('#ff0000' if key in fix else '#ffffff') for key in embedding.vertices()}, text={key: key for key in fix})

    plotter.show()