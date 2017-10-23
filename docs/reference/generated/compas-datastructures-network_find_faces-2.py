<<<<<<< HEAD
# leaves as breakpoints

import compas
from compas.datastructures import FaceNetwork
from compas.datastructures import network_find_faces
from compas.visualization import FaceNetworkPlotter

network = FaceNetwork.from_obj(compas.get_data('grid_irregular.obj'))

network_find_faces(network, breakpoints=network.leaves())

plotter = FaceNetworkPlotter(network)

plotter.draw_vertices(
    radius=0.075,
    facecolor={key: '#cccccc' for key in network.leaves()}
)
plotter.draw_edges(
    color={(u, v): '#cccccc' for u, v in network.edges()}
)
plotter.draw_faces(
    facecolor={fkey: '#eeeeee' for fkey in network.faces()},
    text={fkey: fkey for fkey in network.faces()}
)

=======
# leaves as breakpoints

import compas
from compas.datastructures import FaceNetwork
from compas.datastructures import network_find_faces
from compas.visualization import NetworkPlotter

network = FaceNetwork.from_obj(compas.get_data('grid_irregular.obj'))

network_find_faces(network, breakpoints=network.leaves())

plotter = NetworkPlotter(network)

plotter.draw_vertices(radius=0.075, facecolor={key: '#cccccc' for key in network.leaves()})
plotter.draw_edges(color={(u, v): '#cccccc' for u, v in network.edges()})
plotter.draw_faces(facecolor={fkey: '#eeeeee' for fkey in network.faces()}, text={fkey: fkey for fkey in network.faces()})

>>>>>>> f771242a02ffb1c1d3fab21eccdf9d53daf0a4fd
plotter.show()