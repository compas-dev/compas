import compas
from compas_blender.helpers import NetworkArtist
from compas.datastructures import Network
from compas.numerical import fd_numpy


__author__    = ['Tom Van Mele', 'Andrew Liew']
__copyright__ = 'Copyright 2017, BRG - ETH Zurich',
__license__   = 'MIT'
__email__     = 'van.mele@arch.ethz.ch'


# make a network from sample data

network = Network.from_obj(compas.get_data('saddle.obj'))

# set default vertex and edge attributes

dva = {'is_anchor': False, 'px': 0.0, 'py': 0.0, 'pz': 0.0}
dea = {'q': 1.0}

network.update_default_vertex_attributes(dva)
network.update_default_edge_attributes(dea)

# identify *anchored* vertices

for key in network.vertices():
    network.vertex[key]['is_anchor'] = network.is_vertex_leaf(key)

# convert network data to numerical data

xyz   = network.get_vertices_attributes(('x', 'y', 'z'))
loads = network.get_vertices_attributes(('px', 'py', 'pz'))
q     = network.get_edges_attribute('q')

# use a key-index map to reference items in the numerical data

key_index = network.key_index()

fixed = [key for key in network.vertices() if network.vertex[key]['is_anchor']]
fixed = [key_index[key] for key in fixed]

edges = [(key_index[u], key_index[v]) for u, v in network.edges()]

# run the force density method

res = fd_numpy(xyz, edges, fixed, q, loads)
xyz = res[0]

# update the network

for key in network.vertices():
    index = key_index[key]
    network.vertex[key]['x'] = xyz[index][0]
    network.vertex[key]['y'] = xyz[index][1]
    network.vertex[key]['z'] = xyz[index][2]

# display the result

networkartist = NetworkArtist(network=network)
networkartist.clear_layer()

networkartist.draw_vertices(radius=0.05)
networkartist.draw_vertexlabels()

networkartist.draw_edges()
networkartist.draw_edgelabels()
