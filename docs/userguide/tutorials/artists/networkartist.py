from compas.geometry import Pointcloud
from compas.datastructures import Network
from compas.scene import SceneObject
from compas.colors import Color

network = Network.from_pointcloud(Pointcloud.from_bounds(8, 5, 3, 53))

node = network.node_sample(size=1)[0]
nbrs = network.neighbors(node)
edges = network.connected_edges(node)

SceneObject.clear()

artist = SceneObject(network)
artist.draw(
    nodecolor={n: Color.pink() for n in [node] + nbrs},
    edgecolor={e: Color.pink() for e in edges},
    nodetext='index'
)

SceneObject.redraw()
