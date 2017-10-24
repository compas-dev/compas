"""A dynamic relaxation example comparing NumPy with Numba."""

from compas_blender.geometry import update_bmesh_vertices
from compas_blender.helpers import network_from_bmesh
from compas_blender.utilities import clear_layers
from compas_blender.utilities import draw_plane

from compas.numerical.methods.drx import drx as numpy_drx
from compas.hpc.numba_.drx import numba_drx

from time import time

from matplotlib import pyplot as plt


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


data = {'numpy': [], 'numba': [], 'nodes': []}

# Analysis loop

for m in range(10, 51, 5):

    print('Grid bays : {0}'.format(m))
    clear_layers(layers=[0])

    # Set-up Network

    ds = 1. / m
    bmesh = draw_plane(dx=ds, dy=ds)
    network = network_from_bmesh(bmesh)
    n = network.number_of_vertices()
    network.update_default_vertex_attributes({'B': [0, 0, 1], 'P': [0, 0, 100. / n]})
    network.update_default_edge_attributes({'E': 10, 'A': 1, 'ct': 't', 'l0': ds})
    for key in network.vertices():
        x, y, z = network.vertex_coordinates(key)
        if (x in [0, 1]) and (y in [0, 1]):
            network.set_vertex_attributes(key, {'B': [0, 0, 0]})

    data['nodes'].append(n)

    # Numpy-SciPy

    tic = time()
    X, f, l = numpy_drx(network=network, tol=0.01)
    update_bmesh_vertices(bmesh=bmesh, X=X, winswap=True)
    data['numpy'].append(time() - tic)

    # Numba

    tic = time()
    X, f, l = numba_drx(network=network, tol=0.01)
    update_bmesh_vertices(bmesh=bmesh, X=X, winswap=True)
    data['numba'].append(time() - tic)

# Plot data

plt.plot(data['nodes'], data['numpy'])
plt.plot(data['nodes'], data['numba'])
plt.ylabel('Analysis time [s]')
plt.xlabel('No. nodes')
plt.legend(['NumPy-SciPy', 'Numba'])
plt.xlim([0, data['nodes'][-1]])
plt.ylim([0, max(data['numpy'])])
plt.show()
