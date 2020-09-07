from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import ast
import rhinoscriptsyntax as rs


__all__ = [
    'mesh_select_vertex',
    'mesh_select_vertices',
    'mesh_select_face',
    'mesh_select_faces',
    'mesh_select_edge',
    'mesh_select_edges',
    'network_select_node',
    'network_select_nodes',
    'network_select_edge',
    'network_select_edges',
]


def mesh_select_vertex(mesh, message="Select a vertex."):
    """Select a single vertex of a mesh.

    Parameters
    ----------
    mesh: :class:`compas.datastructures.Mesh`
    message: str, optional

    Returns
    -------
    int or None
    """
    guid = rs.GetObject(message, preselect=True, filter=rs.filter.point | rs.filter.textdot)
    if guid:
        prefix = mesh.attributes['name']
        name = rs.ObjectName(guid).split('.')
        if 'vertex' in name:
            if not prefix or prefix in name:
                key = name[-1]
                return ast.literal_eval(key)
    return None


def mesh_select_vertices(mesh, message="Select vertices."):
    """Select multiple vertices of a mesh.

    Parameters
    ----------
    mesh: :class:`compas.datastructures.Mesh`
    message: str, optional

    Returns
    -------
    list of int
    """
    keys = []
    guids = rs.GetObjects(message, preselect=True, filter=rs.filter.point | rs.filter.textdot)
    if guids:
        prefix = mesh.attributes['name']
        seen = set()
        for guid in guids:
            name = rs.ObjectName(guid).split('.')
            if 'vertex' in name:
                if not prefix or prefix in name:
                    key = name[-1]
                    if not seen.add(key):
                        key = ast.literal_eval(key)
                        keys.append(key)
    return keys


def mesh_select_face(mesh, message="Select a face."):
    """Select a single face of a mesh.

    Parameters
    ----------
    mesh: :class:`compas.datastructures.Mesh`
    message: str, optional

    Returns
    -------
    int or None
    """
    guid = rs.GetObject(message, preselect=True, filter=rs.filter.mesh | rs.filter.textdot)
    if guid:
        prefix = mesh.attributes['name']
        name = rs.ObjectName(guid).split('.')
        if 'face' in name:
            if not prefix or prefix in name:
                key = name[-1]
                key = ast.literal_eval(key)
                return key
    return None


def mesh_select_faces(mesh, message="Select faces."):
    """Select multiple faces of a mesh.

    Parameters
    ----------
    mesh: :class:`compas.datastructures.Mesh`
    message: str, optional

    Returns
    -------
    list of int
    """
    keys = []
    guids = rs.GetObjects(message, preselect=True, filter=rs.filter.mesh | rs.filter.textdot)
    if guids:
        prefix = mesh.attributes['name']
        seen = set()
        for guid in guids:
            name = rs.ObjectName(guid).split('.')
            if 'face' in name:
                if not prefix or prefix in name:
                    key = name[-1]
                    if not seen.add(key):
                        key = ast.literal_eval(key)
                        keys.append(key)
    return keys


def mesh_select_edge(mesh, message="Select an edge."):
    """Select a single edge of a mesh.

    Parameters
    ----------
    mesh: :class:`compas.datastructures.Mesh`
    message: str, optional

    Returns
    -------
    tuple of int, or None
    """
    guid = rs.GetObject(message, preselect=True, filter=rs.filter.curve | rs.filter.textdot)
    if guid:
        prefix = mesh.attributes['name']
        name = rs.ObjectName(guid).split('.')
        if 'edge' in name:
            if not prefix or prefix in name:
                key = name[-1]
                u, v = key.split('-')
                u = ast.literal_eval(u)
                v = ast.literal_eval(v)
                return u, v
    return None


def mesh_select_edges(mesh, message="Select edges."):
    """Select multiple edges of a mesh.

    Parameters
    ----------
    mesh: :class:`compas.datastructures.Mesh`
    message: str, optional

    Returns
    -------
    list of tuple of int
    """
    keys = []
    guids = rs.GetObjects(message, preselect=True, filter=rs.filter.curve | rs.filter.textdot)
    if guids:
        prefix = mesh.attributes['name']
        seen = set()
        for guid in guids:
            name = rs.ObjectName(guid).split('.')
            if 'edge' in name:
                if not prefix or prefix in name:
                    key = name[-1]
                    if not seen.add(key):
                        u, v = key.split('-')
                        u = ast.literal_eval(u)
                        v = ast.literal_eval(v)
                        keys.append((u, v))
    return keys


def network_select_node(network, message="Select a node."):
    """Select a single node of a network.

    Parameters
    ----------
    network: :class:`compas.datastructures.Network`
    message: str, optional

    Returns
    -------
    hashable or None
    """
    guid = rs.GetObject(message, preselect=True, filter=rs.filter.point | rs.filter.textdot)
    if guid:
        prefix = network.attributes['name']
        name = rs.ObjectName(guid).split('.')
        if 'node' in name:
            if not prefix or prefix in name:
                key = name[-1]
                return ast.literal_eval(key)
    return None


def network_select_nodes(network, message="Select nodes."):
    """Select multiple nodes of a network.

    Parameters
    ----------
    network: :class:`compas.datastructures.Network`
    message: str, optional

    Returns
    -------
    list of hashable
    """
    keys = []
    guids = rs.GetObjects(message, preselect=True, filter=rs.filter.point | rs.filter.textdot)
    if guids:
        prefix = network.attributes['name']
        seen = set()
        for guid in guids:
            name = rs.ObjectName(guid).split('.')
            if 'node' in name:
                if not prefix or prefix in name:
                    key = name[-1]
                    if not seen.add(key):
                        key = ast.literal_eval(key)
                        keys.append(key)
    return keys


def network_select_edge(network, message="Select an edge."):
    """Select a single edge of a network.

    Parameters
    ----------
    network: :class:`compas.datastructures.Network`
    message: str, optional

    Returns
    -------
    tuple of hashable, or None
    """
    guid = rs.GetObject(message, preselect=True, filter=rs.filter.curve | rs.filter.textdot)
    if guid:
        prefix = network.attributes['name']
        name = rs.ObjectName(guid).split('.')
        if 'edge' in name:
            if not prefix or prefix in name:
                key = name[-1]
                u, v = key.split('-')
                u = ast.literal_eval(u)
                v = ast.literal_eval(v)
                return u, v
    return None


def network_select_edges(network, message="Select edges."):
    """Select multiple edges of a network.

    Parameters
    ----------
    network: :class:`compas.datastructures.Network`
    message: str, optional

    Returns
    -------
    list of tuple of hashable
    """
    keys = []
    guids = rs.GetObjects(message, preselect=True, filter=rs.filter.curve | rs.filter.textdot)
    if guids:
        prefix = network.attributes['name']
        seen = set()
        for guid in guids:
            name = rs.ObjectName(guid).split('.')
            if 'edge' in name:
                if not prefix or prefix in name:
                    key = name[-1]
                    if not seen.add(key):
                        u, v = key.split('-')
                        u = ast.literal_eval(u)
                        v = ast.literal_eval(v)
                        keys.append((u, v))
    return keys


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
