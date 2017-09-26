import rhinoscriptsyntax as rs
from compas.datastructures.network import Network
from compas.utilities import geometric_key

__author__    = 'Tomas Mendez Echenagucia'
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'mendez@arch.ethz.ch'


__all__ = [
    'make_gkdict',
    'from_lines',
    'update_network_edge_attributes',
    'update_network_vertex_attributes',
    'draw_network'
]

# 'update_network_face_attributes',
# 'move_network',
# 'move_network_vertex',
# 'display_network_vertex_labels',
# 'display_network_edge_labels',
# 'display_network_face_labels',
# 'display_network_axial_forces',
# 'display_network_reaction_forces',
# 'display_network_residual_forces',
# 'display_network_selfweight',
# 'display_network_applied_loads',


def make_gkdict(network, precision='3f'):
    gkdict = {}
    for key in network.vertex:
        xyz = network.get_vertex_attributes(key, ['x', 'y', 'z'])
        gk = geometric_key(xyz=xyz, precision=precision)
        gkdict[gk] = key
    return gkdict


def draw_network(network):
    edges = network.edges()
    lines = []
    for u, v in edges:
        u = network.get_vertex_attributes(u, ['x', 'y', 'z'])
        v = network.get_vertex_attributes(v, ['x', 'y', 'z'])
        lines.append(rs.AddLine(u, v))
    return lines


def from_lines(guids):
    lines = [[rs.CurveStartPoint(g), rs.CurveEndPoint(g)] for g in guids]
    network = Network.from_lines(lines)
    return network


def update_network_edge_attributes(network, lines, name, values):
    gkdict = make_gkdict(network, precision='3f')
    if len(values) == 1:
        values = [values[0]] * len(lines)
    for i, line in enumerate(lines):
        value = values[i]
        u = gkdict[geometric_key(rs.CurveStartPoint(line), precision='3f')]
        v = gkdict[geometric_key(rs.CurveEndPoint(line), precision='3f')]
        network.set_edge_attribute(u, v, name, value)


def update_network_vertex_attributes(network, points, name, values):
    gkdict = make_gkdict(network, precision='3f')
    if len(values) == 1:
        values = [values[0]] * len(points)
    for i, point in enumerate(points):
        value = values[i]
        u = gkdict[geometric_key(point, precision='3f')]
        network.set_vertex_attribute(u, name, value)


def move_network(network, vector):
    """Move the entire network.

    Parameters:
        network (compas.datastructures.network.Network): A network object.
        vector (list, tupple): The displacement vector.

    """

    for key, attr in network.vertices(True):
        attr['x'] += vector[0]
        attr['y'] += vector[1]
        attr['z'] += vector[2]


def move_network_vertex(network, points, vectors):
    """Move the entire network.

    Parameters:
        network (compas.datastructures.network.Network): A network object.
        vector (list, tupple): The displacement vector.

    """
    gkdict = make_gkdict(network, precision='3f')
    if len(vectors) == 1:
        vectors = [vectors[0]] * len(points)
    for i, point in enumerate(points):
        u = gkdict[geometric_key(point, precision='3f')]
        vector = vectors[i]
        network.vertex[u]['x'] += vector[0]
        network.vertex[u]['y'] += vector[1]
        network.vertex[u]['z'] += vector[2]
