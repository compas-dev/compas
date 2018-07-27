from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import ctypes
import compas

from compas.datastructures import Network
from compas.plotters import NetworkPlotter
from compas.utilities import i_to_red

from compas.interop.cpp.xdarray import Array2D
from compas.interop.cpp.xdarray import Array1D

lib = ctypes.cdll.LoadLibrary('fd.so')

network = Network.from_obj(compas.get('saddle.obj'))

vertices = network.get_vertices_attributes('xyz')
loads = network.get_vertices_attributes(('px', 'py', 'pz'), (0.0, 0.0, 0.0))
edges = list(network.edges())
fixed = network.leaves()
free = [i for i in range(len(vertices)) if i not in fixed]
q = network.get_edges_attribute('q', 1.0)

cvertices = Array2D(vertices, 'double')
cedges = Array2D(edges, 'int')
cloads = Array2D(loads, 'double')
cq = Array1D(q, 'double')
cfixed = Array1D(fixed, 'int')
cfree = Array1D(free, 'int')

lib.fd.argtypes = [
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    cvertices.ctype,
    cedges.ctype,
    cloads.ctype,
    cq.ctype,
    cfixed.ctype,
    cfree.ctype
]

lib.fd(
    ctypes.c_int(len(vertices)),
    ctypes.c_int(len(edges)),
    ctypes.c_int(len(fixed)),
    cvertices.cdata,
    cedges.cdata,
    cloads.cdata,
    cq.cdata,
    cfixed.cdata,
    cfree.cdata
)

xyz = cvertices.pydata

for key, attr in network.vertices(True):
    attr['x'] = float(xyz[key][0])
    attr['y'] = float(xyz[key][1])
    attr['z'] = float(xyz[key][2])


zmax = max(network.get_vertices_attribute('z'))

plotter = NetworkPlotter(network, figsize=(10, 7))
plotter.draw_vertices(
    facecolor={key: i_to_red(attr['z'] / zmax) for key, attr in network.vertices(True)}
)
plotter.draw_edges()
plotter.show()
