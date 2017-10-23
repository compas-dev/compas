"""A dynamic relaxation example comparing NumPy with Numba."""

from compas_blender.geometry import BlenderMesh
from compas_blender.helpers import network_from_bmesh
from compas_blender.utilities import clear_layer
from compas_blender.utilities import draw_plane

from compas.numerical import drx as numpy_drx
from compas.hpc import numba_drx

from time import time

from matplotlib import pyplot as plt


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


data = {'numpy': [], 'numba': [], 'nodes': []}

for m in range(10, 91, 5):

    clear_layer(layer=0)

    # Set-up Network

    bmesh = draw_plane(dx=1/m, dy=1/m)
    blendermesh = BlenderMesh(object=bmesh)

    network = network_from_bmesh(bmesh=bmesh)
    Pz = 100 / network.number_of_vertices()
    network.update_default_vertex_attributes({'B': [0, 0, 1], 'P': [0, 0, Pz]})
    network.update_default_edge_attributes({'E': 10, 'A': 1, 'ct': 't', 'l0': 1/m})
    corners = [key for key in network.vertices() if network.vertex_degree(key) == 2]
    network.set_vertices_attributes(corners, {'B': [0, 0, 0]})

    data['nodes'].append(network.number_of_vertices())

    # Numpy-SciPy

    tic = time()
    X, f, l = numpy_drx(network=network, tol=0.01)
    data['numpy'].append(time() - tic)
    blendermesh.update_vertices(X)

    # Numba

    tic = time()
    X, f, l = numba_drx(network=network, tol=0.01)
    data['numba'].append(time() - tic)
    blendermesh.update_vertices(X)

# Plot data

plt.plot(data['nodes'], data['numpy'])
plt.plot(data['nodes'], data['numba'])
plt.ylabel('Analysis time [s]')
plt.xlabel('No. nodes')
plt.legend(['NumPy-SciPy', 'Numba'])
plt.xlim([0, data['nodes'][-1]])
plt.ylim([0, max(data['numpy'])])
plt.show()
