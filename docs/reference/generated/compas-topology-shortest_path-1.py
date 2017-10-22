import compas

from compas.datastructures import Network
from compas.topology import shortest_path
from compas.visualization import NetworkPlotter

network = Network.from_obj(compas.get_data('grid_irregular.obj'))

adjacency = {key: network.vertex_neighbours(key) for key in network.vertices()}

start = 21
end = 2

path = shortest_path(adjacency, start, end)

edges = []
for i in range(len(path) - 1):
    u = path[i]
    v = path[i + 1]
    if v not in network.edge[u]:
        u, v = v, u
    edges.append([u, v])

plotter = NetworkPlotter(network)

plotter.draw_vertices(
    text={key: key for key in path},
    facecolor={key: '#ff0000' for key in (path[0], path[-1])},
    radius=0.15
)

plotter.draw_edges(
    color={(u, v): '#ff0000' for u, v in edges},
    width={(u, v): 2.0 for u, v in edges}
)

plotter.show()