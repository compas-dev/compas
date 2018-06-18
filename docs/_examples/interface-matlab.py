"""Interface 01: Matlab

- create Matlab object and connect to an existing shared session
- make a network from sample data
- extract network vertex coordinates and connectivity matrix
- convert to Matlab matrices
- compute coordinate differences in Matlab
- compute edge lengths in Python
- plot results as edge labels


.. note::

    Connect to an existing shared Matlab session if possible, because starting
    the engine from scratch can take some time.

    To create a shared session, open Matlab and run ``matlab.engine.shareEngine``.

"""

from __future__ import print_function

import compas

from compas.com import MatlabEngine
from compas.datastructures import Network
from compas.numerical import connectivity_matrix
from compas.numerical import normrow
from compas.plotters import NetworkPlotter


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2017, BRG - ETH Zurich',
__license__   = 'MIT'
__email__     = 'van.mele@arch.ethz.ch'


# create a Matlab object
# and connect to existing shared session if possible

matlab = MatlabEngine()
matlab.connect()

# make a network from sample data

network = Network.from_obj(compas.get('grid_irregular.obj'))

# extract vertex coordinates and connectivity matrix
# and convert to Matlab matrices

key_index = network.key_index()

xyz = network.get_vertices_attributes('xyz')
xyz = matlab.double(xyz)

edges = [(key_index[u], key_index[v]) for u, v in network.edges()]

C = connectivity_matrix(edges, rtype='list')
C = matlab.double(C)

# compute coordinate differences in Matlab

# # using an engine function
# uv = matlab.engine.mtimes(C, xyz)

# using workspace data
matlab.engine.workspace['C'] = C
matlab.engine.workspace['xyz'] = xyz

uv = matlab.engine.eval('C * xyz')

# compute edge lengths in Python

l = normrow(uv)
l = l.flatten().tolist()

# plot results as edge labels

plotter = NetworkPlotter(network, figsize=(10, 7), fontsize=6)

plotter.draw_vertices()
plotter.draw_edges(text={(u, v): '%.1f' % l[index] for index, (u, v) in enumerate(network.edges())})

plotter.show()
