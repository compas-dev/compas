from numpy import array

import compas
from compas.datastructures import Network
from compas.numerical import network_laplacian_matrix

network = Network.from_obj(compas.get('grid_irregular.obj'))

xy = array([network.vertex_coordinates(key, 'xy') for key in network.vertices()])
L  = network_laplacian_matrix(network, normalize=True, rtype='csr')
d  = L.dot(xy)

lines = [{'start': xy[i], 'end': xy[i] - d[i]} for i, k in enumerate(network.vertices())]