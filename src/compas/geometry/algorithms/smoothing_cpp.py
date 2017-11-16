from __future__ import print_function
from __future__ import absolute_import

import os
import ctypes
from ctypes import *

from compas.interop.core.cpp.xdarray import Array1D
from compas.interop.core.cpp.xdarray import Array2D

# from compas.topology import adjacency_from_edges

HERE = os.path.dirname(__file__)

SO = os.path.join(HERE, '_smoothing_cpp', 'smoothing.so')
DLL = os.path.join(HERE, '_smoothing_cpp', 'smoothing.dll')


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>']
__copyright__  = 'Copyright 2017, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'smooth_centroid_cpp',
]


def smooth_centroid_cpp(vertices, adjacency, fixed, kmax=100, callback=None, callback_args=None):
    """
    """
    try:
        smooth_centroid = ctypes.cdll.LoadLibrary(SO)
    except Exception:
        try:
            smooth_centroid = ctypes.cdll.LoadLibrary(DLL)
        except Exception:
            print(SO)
            print(DLL)
            raise
    # --------------------------------------------------------------------------
    # callback
    # --------------------------------------------------------------------------
    if callback:
        assert callable(callback), 'The provided callback is not callable.'

    v = len(vertices)
    nbrs = [len(adjacency[i]) for i in range(v)]
    neighbours = [adjacency[i] + [0] * (10 - nbrs[i]) for i in range(v)]
    fixed = [i in fixed for i in range(v)]
    # --------------------------------------------------------------------------
    # call
    # --------------------------------------------------------------------------
    c_nbrs = Array1D(nbrs, 'int')
    c_fixed = Array1D(fixed, 'int')
    c_vertices = Array2D(vertices, 'double')
    c_neighbours = Array2D(neighbours, 'int')
    c_callback = CFUNCTYPE(None, c_int)

    mesh, plotter = callback_args

    def wrapper(k):
        print(k)
        xyz = c_vertices.pydata
        callback(xyz)

    smooth_centroid.smooth_centroid.argtypes = [
        c_int,
        c_nbrs.ctype,
        c_fixed.ctype,
        c_vertices.ctype,
        c_neighbours.ctype,
        c_int,
        c_callback
    ]

    smooth_centroid.smooth_centroid(
        c_int(v),
        c_nbrs.cdata,
        c_fixed.cdata,
        c_vertices.cdata,
        c_neighbours.cdata,
        c_int(kmax),
        c_callback(wrapper)
    )

    return c_vertices.pydata


# ==============================================================================
# Testing
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures import Mesh
    from compas.plotters import MeshPlotter
    from compas.geometry import smooth_centroid_cpp

    # make a mesh
    # and set the default vertex and edge attributes

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    dva = {'is_fixed': False, }

    mesh.update_default_vertex_attributes(dva)

    # identify the fixed vertices
    # and assign random prescribed force densities to the edges

    for key, attr in mesh.vertices(True):
        attr['is_fixed'] = mesh.vertex_degree(key) == 2

    # extract numerical data from the datastructure

    vertices  = mesh.get_vertices_attributes(('x', 'y', 'z'))
    edges     = list(mesh.edges())
    fixed     = list(mesh.vertices_where({'is_fixed': True}))
    adjacency = [mesh.vertex_neighbours(key) for key in mesh.vertices()]

    v = len(vertices)

    # make a plotter for (dynamic) visualization
    # and define a callback function
    # for plotting the intermediate configurations

    plotter = MeshPlotter(mesh, figsize=(10, 6))

    def callback(xyz):
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

    # # draw the vertices and edges in the starting configuration
    # # and pause for a second before starting the dynamic visualization

    plotter.draw_vertices(facecolor={key: '#000000' for key in mesh.vertices_where({'is_fixed': True})})
    plotter.draw_edges()

    plotter.update(pause=0.5)

    # run the dynamic relaxation

    xyz = smooth_centroid_cpp(vertices, adjacency, fixed, kmax=50, callback=callback, callback_args=(mesh, plotter))

    # update vertices and edges to reflect the end result

    for key, attr in mesh.vertices(True):
        attr['x'] = xyz[key][0]
        attr['y'] = xyz[key][1]
        attr['z'] = xyz[key][2]

    # # visualize the final geometry

    plotter.clear_vertices()
    plotter.clear_edges()

    plotter.draw_vertices(facecolor={key: '#000000' for key in mesh.vertices_where({'is_fixed': True})})
    plotter.draw_edges()

    plotter.update(pause=1.0)
    plotter.show()
