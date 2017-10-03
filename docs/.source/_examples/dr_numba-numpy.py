"""A dynamic relaxation example comparing NumPy with Numba."""

from compas_blender.helpers import network_from_bmesh
from compas_blender.utilities import draw_plane
from compas_blender.utilities import clear_layers

from compas.numerical.methods.dynamic_relaxation import dr_run
from compas.numerical.hpc.numba.dynamic_relaxation import numba_dr_run

from time import time

from matplotlib import pyplot as plt


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


# Start loop

results = {'numpy': [], 'numba': [], 'nodes': []}
for div in list(range(5, 101, 5)):
    L = 10
    ds = L / div
    print('ds:{0}'.format(ds))

    # Set-up Network

    network = network_from_bmesh(draw_plane(Lx=L, Ly=L, dx=ds, dy=ds))
    keys = list(network.vertices())
    edges = list(network.edges())
    network.set_vertices_attributes(keys, {'B': [0, 0, 1]})
    network.set_edges_attributes(edges, {'E': 100, 'A': 1, 'ct': 't', 'l0': ds})
    for key in network.vertices():
        x, y, z = network.vertex_coordinates(key)
        if (x in [0, 10]) and (y in [0, 10]):
            network.set_vertex_attributes(key, {'B': [0, 0, 0]})
        if (int(x) in range(11)) or (int(y) in range(11)):
            network.set_vertex_attributes(key, {'P': [0, 0, 1]})
    clear_layers([0])

    results['nodes'].append(len(keys))

    # NumPy analysis

    tic = time()
    X, f, l = dr_run(network, refresh=25, tol=0.01, bmesh=True)
    results['numpy'].append(time() - tic)
    clear_layers([19])

    # Numba analysis

    tic = time()
    X, f, l = numba_dr_run(network, summary=1, tol=0.01, bmesh=True)
    clear_layers([19])
    results['numba'].append(time() - tic)

# Plot results

plt.plot(results['nodes'], results['numpy'])
plt.plot(results['nodes'], results['numba'])
plt.ylabel('Analysis time [s]')
plt.xlabel('Number of nodes')
plt.legend(['NumPy-SciPy', 'Numba'])
plt.xlim([0, max(results['nodes'])])
plt.ylim([0, 10])
plt.minorticks_on()
plt.show()
