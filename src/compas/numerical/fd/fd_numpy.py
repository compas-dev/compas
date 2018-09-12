from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import compas

try:
    from numpy import asarray
    from scipy.sparse import diags
    from scipy.sparse.linalg import spsolve

except ImportError:
    compas.raise_if_not_ironpython()

from compas.numerical import connectivity_matrix
from compas.numerical import normrow


__all__ = [
    'fd_numpy',
    'network_fd_numpy',
    'mesh_fd_numpy'
]


def network_fd_numpy_xfunc(data):
    from compas.datastructures import Network
    network = Network.from_data(data)
    network_fd_numpy(network)
    return network.to_data()


def network_fd_numpy(network):
    key_index = network.key_index()
    vertices = network.get_vertices_attributes('xyz')
    edges = [(key_index[u], key_index[v]) for u, v in network.edges()]
    fixed = [key_index[key] for key in network.vertices_where({'is_fixed': True})]
    q = network.get_edges_attribute('q', 1.0)
    loads = network.get_vertices_attributes(('px', 'py', 'pz'), (0.0, 0.0, 0.0))
    xyz, q, f, l, r = fd_numpy(vertices, edges, fixed, q, loads)
    for key, attr in network.vertices(True):
        index = key_index[key]
        attr['x'] = xyz[index][0]
        attr['y'] = xyz[index][1]
        attr['z'] = xyz[index][2]
        attr['rx'] = r[index][0]
        attr['ry'] = r[index][1]
        attr['rz'] = r[index][2]
    for index, (u, v, attr) in enumerate(network.edges(True)):
        attr['f'] = f[index][0]
        attr['l'] = l[index][0]


def mesh_fd_numpy(mesh):
    key_index = mesh.key_index()
    vertices = mesh.get_vertices_attributes('xyz')
    edges = [(key_index[u], key_index[v]) for u, v in mesh.edges()]
    fixed = [key_index[key] for key in mesh.vertices_where({'is_fixed': True})]
    q = mesh.get_edges_attribute('q', 1.0)
    loads = mesh.get_vertices_attributes(('px', 'py', 'pz'), (0.0, 0.0, 0.0))
    xyz, q, f, l, r = fd_numpy(vertices, edges, fixed, q, loads)
    for key, attr in mesh.vertices(True):
        index = key_index[key]
        attr['x'] = xyz[index][0]
        attr['y'] = xyz[index][1]
        attr['z'] = xyz[index][2]
        attr['rx'] = r[index][0]
        attr['ry'] = r[index][1]
        attr['rz'] = r[index][2]
    for index, (u, v, attr) in enumerate(mesh.edges(True)):
        attr['f'] = f[index][0]
        attr['l'] = l[index][0]


def fd_numpy(vertices, edges, fixed, q, loads, **kwargs):
    """Implementation of the force density method to compute equilibrium of axial force networks.

    Parameters
    ----------
    vertices : list
        XYZ coordinates of the vertices of the network
    edges : list
        Edges between vertices represented by
    fixed : list
        Indices of fixed vertices.
    q : list
        Force density of edges.
    loads : list
        XYZ components of the loads on the vertices.

    Returns
    -------
    xyz : array
        XYZ coordinates of the equilibrium geometry.
    q : array
        Force densities in the edges.
    f : array
        Forces in the edges.
    l : array
        Lengths of the edges
    r : array
        Residual forces.

    Notes
    -----
    For more info, see [1]_

    References
    ----------
    .. [1] Schek H., *The Force Density Method for Form Finding and Computation of General Networks*,
           Computer Methods in Applied Mechanics and Engineering 3: 115-134, 1974.

    Examples
    --------
    .. plot::
        :include-source:

        import compas

        from compas.datastructures import Mesh
        from compas.plotters import MeshPlotter
        from compas.numerical import fd_numpy
        from compas.utilities import i_to_black

        # make a mesh
        # add default attributes for form finding

        mesh = Mesh.from_obj(compas.get('faces.obj'))

        mesh.update_default_vertex_attributes({'is_anchor': False, 'px': 0.0, 'py': 0.0, 'pz': 0.0})
        mesh.update_default_edge_attributes({'q': 1.0})

        # identify the anchors
        # move two anchors up to create anticlastic boundary conditions

        for key, attr in mesh.vertices(True):
            attr['is_anchor'] = mesh.vertex_degree(key) == 2
            if key in (18, 35):
                attr['z'] = 5.0

        # preprocess

        k_i   = mesh.key_index()
        xyz   = mesh.get_vertices_attributes(('x', 'y', 'z'))
        loads = mesh.get_vertices_attributes(('px', 'py', 'pz'))
        q     = mesh.get_edges_attribute('q')
        fixed = mesh.vertices_where({'is_anchor': True})
        fixed = [k_i[k] for k in fixed]
        edges = [(k_i[u], k_i[v]) for u, v in mesh.edges()]

        # compute equilibrium
        # update the mesh geometry

        xyz, q, f, l, r = fd_numpy(xyz, edges, fixed, q, loads)

        for key, attr in mesh.vertices(True):
            index = k_i[key]
            attr['x'] = xyz[index, 0]
            attr['y'] = xyz[index, 1]
            attr['z'] = xyz[index, 2]

        # visualisae the result
        # color the vertices according to their elevation

        plotter = MeshPlotter(mesh)

        zmax = max(mesh.get_vertices_attribute('z'))

        plotter.draw_vertices(
            facecolor={key: i_to_black(attr['z'] / zmax) for key, attr in mesh.vertices(True)}
        )
        plotter.draw_faces()
        plotter.draw_edges()
        plotter.show()

    """
    v    = len(vertices)
    free = list(set(range(v)) - set(fixed))
    xyz  = asarray(vertices, dtype=float).reshape((-1, 3))
    q    = asarray(q, dtype=float).reshape((-1, 1))
    p    = asarray(loads, dtype=float).reshape((-1, 3))
    C    = connectivity_matrix(edges, 'csr')
    Ci   = C[:, free]
    Cf   = C[:, fixed]
    Ct   = C.transpose()
    Cit  = Ci.transpose()
    Q    = diags([q.flatten()], [0])
    A    = Cit.dot(Q).dot(Ci)
    b    = p[free] - Cit.dot(Q).dot(Cf).dot(xyz[fixed])

    xyz[free] = spsolve(A, b)

    l = normrow(C.dot(xyz))
    f = q * l
    r = p - Ct.dot(Q).dot(C).dot(xyz)

    return xyz, q, f, l, r


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import compas

    from compas.datastructures import Mesh
    from compas.plotters import MeshPlotter
    from compas.utilities import i_to_rgb

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    mesh.update_default_vertex_attributes({'is_fixed': False, 'px': 0.0, 'py': 0.0, 'pz': 0.0})
    mesh.update_default_edge_attributes({'q': 1.0})

    for key, attr in mesh.vertices(True):
        attr['is_fixed'] = mesh.vertex_degree(key) == 2

    plotter = MeshPlotter(mesh, figsize=(10, 7))

    plotter.draw_as_lines(color='#cccccc', width=0.5)

    network_fd_numpy(mesh)

    zmax = max(mesh.get_vertices_attribute('z'))
    fmax = max(mesh.get_edges_attribute('f'))

    plotter.draw_vertices()
    plotter.draw_faces()
    plotter.draw_edges(
        width={(u, v): 10 * attr['f'] / fmax for u, v, attr in mesh.edges(True)},
        color={(u, v): i_to_rgb(attr['f'] / fmax) for u, v, attr in mesh.edges(True)},
    )

    plotter.show()
