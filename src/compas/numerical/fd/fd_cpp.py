from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import compas

try:
    import ctypes

    from compas.interop.cpp import Array2D
    from compas.interop.cpp import Array1D

except (ImportError, SystemError):
    compas.raise_if_not_ironpython()

HERE = os.path.dirname(__file__)

SO = os.path.join(HERE, '__fd_cpp', 'fd.so')
DLL = os.path.join(HERE, '__fd_cpp', 'fd.dll')


__all__ = ['fd_cpp']


def fd_cpp(vertices, edges, fixed, q, loads, **kwargs):
    try:
        lib = ctypes.cdll.LoadLibrary(SO)
    except Exception:
        try:
            lib = ctypes.cdll.LoadLibrary(DLL)
        except Exception:
            raise

    free = [i for i in range(len(vertices)) if i not in fixed]

    cvertices = Array2D(vertices, 'double')
    cedges    = Array2D(edges, 'int')
    cloads    = Array2D(loads, 'double')
    cq        = Array1D(q, 'double')
    cfixed    = Array1D(fixed, 'int')
    cfree     = Array1D(free, 'int')

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

    return cvertices.pydata


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas.datastructures import Network
    from compas.plotters import NetworkPlotter
    from compas.utilities import i_to_red

    network = Network.from_obj(compas.get('saddle.obj'))

    vertices = network.get_vertices_attributes('xyz')
    loads    = network.get_vertices_attributes(('px', 'py', 'pz'), (0.0, 0.0, 0.0))
    fixed    = network.leaves()
    edges    = list(network.edges())
    q        = network.get_edges_attribute('q', 1.0)

    xyz = fd_cpp(vertices, edges, fixed, q, loads)

    for key, attr in network.vertices(True):
        attr['x'] = xyz[key][0]
        attr['y'] = xyz[key][1]
        attr['z'] = xyz[key][2]

    zmax = max(network.get_vertices_attribute('z'))

    plotter = NetworkPlotter(network, figsize=(10, 7))
    plotter.draw_vertices(
        facecolor={key: i_to_red(attr['z'] / zmax) for key, attr in network.vertices(True)}
    )
    plotter.draw_edges()
    plotter.show()
