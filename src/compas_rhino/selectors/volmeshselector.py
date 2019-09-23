from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


from compas_rhino.selectors import VertexSelector
from compas_rhino.selectors import EdgeSelector
from compas_rhino.selectors import FaceSelector


__all__ = [
    'volmesh_select_vertex',
    'volmesh_select_edge',
    'volmesh_select_edges',
    'volmesh_select_face',
    'volmesh_select_faces',
]

# ==============================================================================
# selections
# ==============================================================================


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


def volmesh_select_edge(volmesh):
    """"""
    return EdgeSelector.select_edge(volmesh)


def volmesh_select_edges(volmesh):
    """"""
    return EdgeSelector.select_edges(volmesh)


def volmesh_select_face(volmesh):
    """"""
    return FaceSelector.select_face(volmesh)


def volmesh_select_faces(volmesh):
    """"""
    return FaceSelector.select_faces(volmesh)


def volmesh_select_cell():
    pass


def volmesh_select_cells():
    pass
