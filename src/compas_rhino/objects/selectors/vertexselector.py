from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import ast

import compas
from compas.utilities import geometric_key


try:
    import rhinoscriptsyntax as rs
except ImportError:
    compas.raise_if_ironpython()


__all__ = [
    'VertexSelector',

    'mesh_identify_vertices',
    'mesh_select_vertices',
    'mesh_select_vertex',

    'network_select_vertices',
    'network_select_vertex',

    'volmesh_select_vertices',
    'volmesh_select_vertex'
    ]


class VertexSelector(object):

    @staticmethod
    def select_vertex(self, message="Select a vertex."):
        guid = rs.GetObject(message, preselect=True, filter=rs.filter.point | rs.filter.textdot)
        if guid:
            prefix = self.attributes['name']
            name = rs.ObjectName(guid).split('.')
            if 'vertex' in name:
                if not prefix or prefix in name:
                    key = name[-1]
                    return ast.literal_eval(key)
        return None

    @staticmethod
    def select_vertices(self, message="Select vertices."):
        keys = []
        guids = rs.GetObjects(message, preselect=True, filter=rs.filter.point | rs.filter.textdot)
        if guids:
            prefix = self.attributes['name']
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


# TODO: make sure if this function should be here
def mesh_identify_vertices(mesh, points, precision=None):
    keys = []
    gkey_key = {geometric_key(mesh.vertex_coordinates(key), precision): key for key in mesh.vertices()}
    for xyz in points:
        gkey = geometric_key(xyz, precision)
        if gkey in gkey_key:
            key = gkey_key[gkey]
            keys.append(key)
    return keys


def mesh_select_vertices(mesh, message="Select mesh vertices."):
    """Select vertices of a mesh.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        A mesh object.
    message : str ("Select mesh vertices.")
        The message to display to the user.

    Returns
    -------
    list
        The keys of the selected vertices.

    See Also
    --------
    * :func:`mesh_select_edges`
    * :func:`mesh_select_faces`

    """
    return VertexSelector.select_vertices(mesh)


def mesh_select_vertex(mesh, message="Select a mesh vertex"):
    """Select one vertex of a mesh.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        A mesh object.
    message : str ("Select a mesh vertex.")
        The message to display to the user.

    Returns
    -------
    hashable
        The key of the selected vertex.

    See Also
    --------
    * :func:`mesh_select_vertices`

    """
    return VertexSelector.select_vertex(mesh)


def network_select_vertices(network, message="Select network vertices."):
    """Select vertices of a network.

    Parameters
    ----------
    network : compas.datastructures.Network
        A network object.
    message : str ("Select network vertices.")
        The message to display to the user.

    Returns
    -------
    list
        The keys of the selected vertices.

    Examples
    --------
    >>>

    See Also
    --------
    * :func:`network_select_vertex`

    """
    return VertexSelector.select_vertices(network)


def network_select_vertex(network, message="Select a network vertex"):
    """Select one vertex of a network.

    Parameters
    ----------
    network : compas.datastructures.Network
        A network object.
    message : str ("Select a network vertex.")
        The message to display to the user.

    Returns
    -------
    str
        The key of the selected vertex.
    None
        If no vertex was selected.

    See Also
    --------
    * :func:`network_select_vertices`

    """
    return VertexSelector.select_vertex(network)


def volmesh_select_vertices(volmesh):
    """Select multiple vertices of a volmesh.

    Parameters
    ----------
    volmesh : compas.datastructures.VolMesh
        A volmesh object.

    Returns
    -------
    keys : list(int, str, tuple, frozenset)
        The identifiers or *keys* of the selected vertices.

    Examples
    --------
    >>> keys = volmesh_select_vertices(volmesh)

    See Also
    --------
    * volmesh_select_vertex

    """
    return VertexSelector.select_vertices(volmesh)


def volmesh_select_vertex(volmesh):
    """Select a vertex of a volmesh.

    Parameters
    ----------
    volmesh : compas.datastructures.VolMesh
        A volmesh object.

    Returns
    -------
    key : int, str, tuple, frozenset
        The identifier or *key* of the selected vertex.
    None
        If no vertex was selected.

    Examples
    --------
    >>> key = volmesh_select_vertex(volmesh)

    See Also
    --------
    * volmesh_select_vertices

    """
    return VertexSelector.select_vertex(volmesh)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
