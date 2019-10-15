from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import ast

import compas

try:
    import rhinoscriptsyntax as rs
except ImportError:
    compas.raise_if_ironpython()


__all__ = [
    'EdgeSelector',

    'mesh_select_edges',
    'mesh_select_edge',

    'network_select_edges',
    'network_select_edge',

    'volmesh_select_edges',
    'volmesh_select_edge'
    ]


class EdgeSelector(object):

    @staticmethod
    def select_edge(self, message="Select an edge."):
        guid = rs.GetObject(message, preselect=True, filter=rs.filter.curve | rs.filter.textdot)
        if guid:
            prefix = self.attributes['name']
            name = rs.ObjectName(guid).split('.')
            if 'edge' in name:
                if not prefix or prefix in name:
                    key = name[-1]
                    u, v = key.split('-')
                    u = ast.literal_eval(u)
                    v = ast.literal_eval(v)
                    return u, v
        return None

    @staticmethod
    def select_edges(self, message="Select edges."):
        keys = []
        guids = rs.GetObjects(message, preselect=True, filter=rs.filter.curve | rs.filter.textdot)
        if guids:
            prefix = self.attributes['name']
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


def mesh_select_edges(mesh, message="Select mesh edges"):
    """Select edges of a mesh.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        A mesh object.
    message : str ("Select mesh edges.")
        The message to display to the user.

    Returns
    -------
    list
        The keys of the selected edges.

    See Also
    --------
    * :func:`mesh_select_vertices`
    * :func:`mesh_select_faces`

    """
    return EdgeSelector.select_edges(mesh)


def mesh_select_edge(mesh, message="Select a mesh edge"):
    """Select one edge of a mesh.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        A mesh object.
    message : str ("Select a mesh edge.")
        The message to display to the user.

    Returns
    -------
    tuple
        The key of the selected edge.

    See Also
    --------
    * :func:`mesh_select_edges`

    """
    return EdgeSelector.select_edge(mesh)


def network_select_edges(network, message="Select network edges"):
    """Select edges of a network.

    Parameters
    ----------
    network : compas.datastructures.Network
        The network object.
    message : str ("Select network edges.")
        The message to display to the user.

    Returns
    -------
    list
        The keys of the selected edges. Each key is a *uv* pair.

    See Also
    --------
    * :func:`network_select_edge`

    """
    return EdgeSelector.select_edges(network)


def network_select_edge(network, message="Select a network edge"):
    """Select one edge of a network.

    Parameters
    ----------
    network : compas.datastructures.Network
        A network object.
    message : str ("Select a network edge.")
        The message to display to the user.

    Returns
    -------
    tuple
        The key of the selected edge.
    None
        If no edge was selected.

    See Also
    --------
    * :func:`network_select_edges`

    """
    return EdgeSelector.select_edge(network)


def volmesh_select_edge(volmesh):
    """"""
    return EdgeSelector.select_edge(volmesh)


def volmesh_select_edges(volmesh):
    """"""
    return EdgeSelector.select_edges(volmesh)

# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
