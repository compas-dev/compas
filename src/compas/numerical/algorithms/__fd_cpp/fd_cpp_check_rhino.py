from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from ctypes import c_double
import random
import compas
import compas_rhino

from compas.datastructures import Network
from compas.numerical import fd_cpp
from compas.utilities import i_to_red

from compas_rhino.helpers import NetworkArtist

network = Network.from_obj(compas.get('saddle.obj'))

# for u, v, attr in network.edges(True):
#     attr['q'] = 1.0 * random.randint(1, 5)

vertices = network.get_vertices_attributes('xyz')
loads    = network.get_vertices_attributes(('px', 'py', 'pz'), (0.0, 0.0, 0.0))
fixed    = network.leaves()
free     = [i for i in range(len(vertices)) if i not in fixed]
edges    = list(network.edges())
q        = network.get_edges_attribute('q', 1.0)


artist = NetworkArtist(network, layer='Network')

artist.clear_layer()
artist.draw_edges(color='#cccccc')
artist.redraw()

xyz = fd_cpp(vertices, edges, fixed, q, loads)

for key, attr in network.vertices(True):
    attr['x'] = xyz[key][0]
    attr['y'] = xyz[key][1]
    attr['z'] = xyz[key][2]

artist.draw_vertices(color={key: '#ff0000' for key in network.leaves()})
artist.draw_edges(color='#000000')
artist.redraw()
