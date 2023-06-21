from compas.geometry import Pointcloud
from compas.datastructures import Network
from compas.artists import Artist
from compas.colors import Color

network = Network.from_pointcloud(Pointcloud.from_bounds(8, 5, 3, 53))

node = network.node_sample(size=1)[0]
nbrs = network.neighbors(node)
edges = network.connected_edges(node)

Artist.clear()

artist = Artist(network)
artist.draw(
    nodecolor={n: Color.pink() for n in [node] + nbrs},
    edgecolor={e: Color.pink() for e in edges},
)

Artist.redraw()
