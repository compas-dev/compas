from __future__ import print_function

from compas_rhino.selectors import VertexSelector
from compas_rhino.selectors import EdgeSelector
from compas_rhino.selectors import FaceSelector


__all__ = [
    'mesh_select_vertices',
    'mesh_select_vertex',
    'mesh_select_edges',
    'mesh_select_edge',
    'mesh_select_faces',
    'mesh_select_face'
]


# ==============================================================================
# selections
# ==============================================================================


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


def mesh_select_faces(mesh, message='Select mesh faces.'):
    """Select faces of a mesh.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        A mesh object.
    message : str ("Select mesh faces.")
        The message to display to the user.

    Returns
    -------
    list
        The keys of the selected faces.

    See Also
    --------
    * :func:`mesh_select_vertices`
    * :func:`mesh_select_edges`

    """
    return FaceSelector.select_faces(mesh)


def mesh_select_face(mesh, message='Select face.'):
    """Select one face of a mesh.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        A mesh object.
    message : str ("Select a mesh face.")
        The message to display to the user.

    Returns
    -------
    hashable
        The key of the selected face.

    See Also
    --------
    * :func:`mesh_select_faces`

    """
    return FaceSelector.select_face(mesh)
