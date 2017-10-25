"""
next steps:
-----------
- default attributes
- vertices_where
- custom class
- random distributions of force densities
- start from basic plot => refine
- tighten cables (find cables)

"""

from __future__ import print_function

import compas

from compas.datastructures import Mesh
from compas.visualization import MeshPlotter
from compas.numerical import fd
from compas.utilities import i_to_rgb
from compas.utilities import pairwise


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


def main():

    # mesh and plotter

    mesh = Mesh.from_obj(compas.get('faces.obj'))
    plotter = MeshPlotter(mesh)

    mesh.update_default_vertex_attributes({'px': 0.0, 'py': 0.0, 'pz': 0.0})
    mesh.update_default_edge_attributes({'q': 1.0})

    # plot original state

    lines = []
    for u, v in mesh.edges():
        lines.append({
            'start': mesh.vertex_coordinates(u, 'xy'),
            'end'  : mesh.vertex_coordinates(v, 'xy'),
            'color': '#cccccc',
            'width': 0.5 
        })

    plotter.draw_lines(lines)

    # find the cables and modify their force densities

    fixed    = [k for k in mesh.vertices() if mesh.vertex_degree(k) == 2]
    boundary = mesh.vertices_on_boundary(ordered=True)
    corners  = sorted(boundary.index(k) for k in fixed)

    cables = []
    for a, b in pairwise(corners):
        cables.append(boundary[a: b + 1])

    cables.append(boundary[corners[-1]: ] + boundary[: corners[0] + 1])

    for cable in cables:
        for u, v in pairwise(cable):
            mesh.set_edge_attribute((u, v), 'q', 3.0, directed=False)
    
    # preprocess

    k_i  = mesh.key_index()
    i_k  = mesh.index_key()
    uv_i = mesh.uv_index()
    i_uv = mesh.index_uv()

    fixed = [k_i[k] for k in fixed]
    xyz   = mesh.get_vertices_attributes('xyz')
    loads = mesh.get_vertices_attributes(('px', 'py', 'pz'))
    edges = mesh.indexed_edges()
    q     = mesh.get_edges_attribute('q')

    # compute equilibrium

    xyz, q, f, l, r = fd(xyz, edges, fixed, q, loads, rtype='list')

    # update

    for key, attr in mesh.vertices(True):
        x, y, z = xyz[k_i[key]]
        attr['x'] = x
        attr['y'] = y
        attr['z'] = z

    # visualize

    fmax = max(f)

    plotter.draw_vertices(
        radius={k: 0.05 if k_i[k] not in fixed else 0.1 for k in mesh.vertices()},
        facecolor={i_k[i]: '#000000' for i in fixed}
    )

    plotter.draw_faces()

    plotter.draw_edges(
        text={uv: '{0:.1f}'.format(f[uv_i[uv]]) for uv in mesh.edges()},
        color={uv: i_to_rgb(f[uv_i[uv]] / fmax) for uv in mesh.edges()},
        width={uv: 10 * f[uv_i[uv]] / fmax for uv in mesh.edges()},
    )

    plotter.show()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    
    main()
