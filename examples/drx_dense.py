#"""A dynamic relaxation example comparing NumPy with Numba."""

from compas_blender.geometry import BlenderMesh
from compas_blender.helpers import network_from_bmesh
from compas_blender.utilities import clear_layer
from compas_blender.utilities import draw_plane

from compas.numerical import drx as numpy_drx
from compas.hpc import numba_drx

from numpy import zeros

from time import time


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


# Callback function

def callback(X, blendermesh):
    blendermesh.update_vertices(X)
    
    
clear_layer(layer=0)
    
# Set-up Network

m = 200
bmesh = draw_plane(dx=1/m, dy=1/m)
blendermesh = BlenderMesh(object=bmesh)

network = network_from_bmesh(bmesh=bmesh)
Pz = 2000 / network.number_of_vertices()
network.update_default_vertex_attributes({'P': [0, 0, Pz]})
network.update_default_edge_attributes({'E': 10, 'A': 1, 'ct': 't', 'l0': 1/m})
corners = [key for key in network.vertices() if network.vertex_degree(key) <= 3]
network.set_vertices_attributes(corners, {'B': [0, 0, 0]})

# Numpy-SciPy

tic = time()
X, f, l = numpy_drx(network=network, tol=0.01, refresh=10, callback=callback, blendermesh=blendermesh)
blendermesh.update_vertices(X)
print('\nNumpy: {0}s\n'.format(time() - tic))

blendermesh.update_vertices(X * 0)

# Numba

tic = time()
X, f, l = numba_drx(network=network, tol=0.01)
blendermesh.update_vertices(X)
print('\nNumba: {0}s\n'.format(time() - tic))