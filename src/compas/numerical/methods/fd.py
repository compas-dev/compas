from numpy import asarray

from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

from compas.numerical.matrices import connectivity_matrix
from compas.numerical.linalg import normrow


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'fd'
]


def fd(vertices, edges, fixed, q, loads, rtype='list'):
    num_v     = len(vertices)
    free      = list(set(range(num_v)) - set(fixed))
    xyz       = asarray(vertices, dtype=float).reshape((-1, 3))
    q         = asarray(q, dtype=float).reshape((-1, 1))
    p         = asarray(loads, dtype=float).reshape((-1, 3))
    C         = connectivity_matrix(edges, 'csr')
    Ci        = C[:, free]
    Cf        = C[:, fixed]
    Ct        = C.transpose()
    Cit       = Ci.transpose()
    Q         = diags([q.flatten()], [0])
    A         = Cit.dot(Q).dot(Ci)
    b         = p[free] - Cit.dot(Q).dot(Cf).dot(xyz[fixed])
    xyz[free] = spsolve(A, b)
    l         = normrow(C.dot(xyz))
    f         = q * l
    r         = p - Ct.dot(Q).dot(C).dot(xyz)
    if rtype == 'list':
        return [xyz.tolist(),
                q.ravel().tolist(),
                f.ravel().tolist(),
                l.ravel().tolist(),
                r.tolist()]
    if rtype == 'dict':
        return {'xyz': xyz.tolist(),
                'q'  : q.ravel().tolist(),
                'f'  : f.ravel().tolist(),
                'l'  : l.ravel().tolist(),
                'r'  : r.tolist()}
    return xyz, q, f, l, r


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    import random

    import compas

    from compas.datastructures import Network
    from compas.visualization.viewers import NetworkViewer

    network = Network.from_obj(compas.get('saddle.obj'))

    network.update_default_vertex_attributes({'is_anchor': False, 'px': 0.0, 'py': 0.0, 'pz': 0.0})
    network.update_default_edge_attributes({'q': 1.0})

    for key, attr in network.vertices(True):
        attr['is_anchor'] = network.is_vertex_leaf(key)

    key = random.choice(network.vertices_where({'is_anchor': False}))

    network.vertex[key]['pz'] = -5.0

    k_i   = network.key_index()

    xyz   = network.get_vertices_attributes(('x', 'y', 'z'))
    loads = network.get_vertices_attributes(('px', 'py', 'pz'))
    q     = network.get_edges_attribute('q')

    fixed = network.vertices_where({'is_anchor': True})
    fixed = [k_i[k] for k in fixed]
    edges = [(k_i[u], k_i[v]) for u, v in network.edges()]

    xyz, q, f, l, r = fd(xyz, edges, fixed, q, loads, rtype='list')

    for key in network.vertices():
        index = k_i[key]
        network.vertex[key]['x'] = xyz[index][0]
        network.vertex[key]['y'] = xyz[index][1]
        network.vertex[key]['z'] = xyz[index][2]

    viewer = NetworkViewer(network)

    viewer.setup()
    viewer.show()
