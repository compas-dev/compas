from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
import os

try:
    import ctypes
    from ctypes import *

    from compas.interop.cpp import Array1D
    from compas.interop.cpp import Array2D

except (ImportError, SystemError):
    compas.raise_if_not_ironpython()


HERE = os.path.dirname(__file__)

SO = os.path.join(HERE, '_smoothing_cpp', 'smoothing.so')
DLL = os.path.join(HERE, '_smoothing_cpp', 'smoothing.dll')


__all__ = [
    'smooth_centroid_cpp',
]


def smooth_centroid_cpp(vertices, adjacency, fixed, kmax=100, callback=None, callback_args=None):
    """
    """
    try:
        smoothing = ctypes.cdll.LoadLibrary(SO)
    except Exception:
        try:
            smoothing = ctypes.cdll.LoadLibrary(DLL)
        except Exception:
            print(SO)
            print(DLL)
            raise
    # --------------------------------------------------------------------------
    # callback
    # --------------------------------------------------------------------------
    if callback:
        assert callable(callback), 'The provided callback is not callable.'
    else:
        def callback(k, xyz):
            pass

    v = len(vertices)
    nbrs = [len(adjacency[i]) for i in range(v)]
    neighbors = [adjacency[i] + [0] * (10 - nbrs[i]) for i in range(v)]
    # --------------------------------------------------------------------------
    # call
    # --------------------------------------------------------------------------
    c_nbrs = Array1D(nbrs, 'int')
    c_fixed = Array1D(fixed, 'int')
    c_vertices = Array2D(vertices, 'double')
    c_neighbors = Array2D(neighbors, 'int')
    c_callback = CFUNCTYPE(None, c_int)

    def wrapper(k):
        callback(k, c_vertices.cdata)

    smoothing.smooth_centroid.argtypes = [
        c_int,
        c_nbrs.ctype,
        c_fixed.ctype,
        c_vertices.ctype,
        c_neighbors.ctype,
        c_int,
        c_callback
    ]

    smoothing.smooth_centroid(
        c_int(v),
        c_nbrs.cdata,
        c_fixed.cdata,
        c_vertices.cdata,
        c_neighbors.cdata,
        c_int(kmax),
        c_callback(wrapper)
    )

    return c_vertices.pydata


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures import Mesh
    from compas.plotters import MeshPlotter

    kmax = 50

    # make a mesh
    # and set the default vertex and edge attributes

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    # extract numerical data from the datastructure

    vertices  = mesh.get_vertices_attributes(('x', 'y', 'z'))
    adjacency = [mesh.vertex_neighbors(key) for key in mesh.vertices()]
    fixed     = [int(mesh.vertex_degree(key) == 2) for key in mesh.vertices()]

    slider = list(mesh.vertices_where({'x': (-0.1, 0.1), 'y': (9.9, 10.1)}))[0]

    # make a plotter for (dynamic) visualization
    # and define a callback function
    # for plotting the intermediate configurations

    plotter = MeshPlotter(mesh, figsize=(10, 7))

    def callback(k, xyz):
        print(k)

        if k < kmax - 1:
            xyz[slider][0] = 0.1 * (k + 1)

        plotter.update_vertices()
        plotter.update_edges()
        plotter.update(pause=0.001)

        for key, attr in mesh.vertices(True):
            attr['x'] = xyz[key][0]
            attr['y'] = xyz[key][1]
            attr['z'] = xyz[key][2]

    # plot the lines of the original configuration of the mesh
    # as a reference

    lines = []
    for u, v in mesh.edges():
        lines.append({
            'start': mesh.vertex_coordinates(u, 'xy'),
            'end'  : mesh.vertex_coordinates(v, 'xy'),
            'color': '#cccccc',
            'width': 0.5
        })

    plotter.draw_lines(lines)

    # draw the vertices and edges in the starting configuration
    # and pause for a second before starting the dynamic visualization

    plotter.draw_vertices(facecolor={key: '#000000' for key in mesh.vertices() if mesh.vertex_degree(key) == 2})
    plotter.draw_edges()

    plotter.update(pause=0.5)

    # run the smoother

    xyz = smooth_centroid_cpp(vertices, adjacency, fixed, kmax=kmax, callback=callback)

    # keep the plot alive

    plotter.show()
