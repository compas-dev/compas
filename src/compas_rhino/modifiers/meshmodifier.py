from __future__ import print_function

from compas.utilities import geometric_key

from compas_rhino.modifiers import Modifier
from compas_rhino.modifiers import VertexModifier
from compas_rhino.modifiers import EdgeModifier
from compas_rhino.modifiers import FaceModifier


__all__ = [
    'mesh_update_vertex_attributes',
    'mesh_update_edge_attributes',
    'mesh_update_face_attributes',
    'mesh_move_vertex',
    'mesh_move_vertices',
    'mesh_identify_vertices',
]


# ==============================================================================
# modifications
# ==============================================================================


def mesh_update_attributes(mesh):
    """Update the attributes of a mesh.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        A mesh object.

    Returns
    -------
    bool
        ``True`` if the update was successful.
        ``False`` otherwise.

    See Also
    --------
    * :func:`mesh_update_vertex_attributes`
    * :func:`mesh_update_edge_attributes`
    * :func:`mesh_update_face_attributes`

    """
    return Modifier.update_attributes(mesh)


def mesh_update_vertex_attributes(mesh, keys, names=None):
    """Update the attributes of the vertices of a mesh.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        A mesh object.
    keys : tuple, list
        The keys of the vertices to update.
    names : tuple, list (None)
        The names of the atrtibutes to update.
        Default is to update all attributes.

    Returns
    -------
    bool
        ``True`` if the update was successful.
        ``False`` otherwise.

    See Also
    --------
    * :func:`mesh_update_attributes`
    * :func:`mesh_update_edge_attributes`
    * :func:`mesh_update_face_attributes`

    """
    return VertexModifier.update_vertex_attributes(mesh, keys, names=names)


def mesh_move_vertex(mesh, key, constraint=None, allow_off=False):
    """Move on vertex of the mesh.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        A mesh object.
    key : str
        The vertex to move.
    constraint : Rhino.Geometry (None)
        A Rhino geometry object to constrain the movement to.
        By default the movement is unconstrained.
    allow_off : bool (False)
        Allow the vertex to move off the constraint.

    """
    return VertexModifier.move_vertex(mesh, key, constraint=constraint, allow_off=allow_off)


def mesh_move_vertices(mesh, keys):
    """Move on vertices of the mesh.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        A mesh object.
    keys : list
        The vertices to move.
    constraint : Rhino.Geometry (None)
        A Rhino geometry object to constrain the movement to.
        By default the movement is unconstrained.
    allow_off : bool (False)
        Allow the vertex to move off the constraint.

    """
    return VertexModifier.move_vertices(mesh, keys)


def mesh_update_edge_attributes(mesh, keys, names=None):
    """Update the attributes of the edges of a mesh.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        A mesh object.
    keys : tuple, list
        The keys of the edges to update.
    names : tuple, list (None)
        The names of the atrtibutes to update.
        Default is to update all attributes.

    Returns
    -------
    bool
        ``True`` if the update was successful.
        ``False`` otherwise.

    See Also
    --------
    * :func:`mesh_update_attributes`
    * :func:`mesh_update_vertex_attributes`
    * :func:`mesh_update_face_attributes`

    """
    return EdgeModifier.update_edge_attributes(mesh, keys, names=names)


def mesh_update_face_attributes(mesh, fkeys, names=None):
    """Update the attributes of the faces of a mesh.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        A mesh object.
    fkeys : tuple, list
        The keys of the faces to update.
    names : tuple, list (None)
        The names of the atrtibutes to update.
        Default is to update all attributes.

    Returns
    -------
    bool
        ``True`` if the update was successful.
        ``False`` otherwise.

    See Also
    --------
    * :func:`mesh_update_attributes`
    * :func:`mesh_update_vertex_attributes`
    * :func:`mesh_update_edge_attributes`

    """
    return FaceModifier.update_vertex_attributes(mesh, fkeys, names=names)


# ==============================================================================
# identify
# ==============================================================================


def mesh_identify_vertices(mesh, points, precision=None):
    keys = []
    gkey_key = {geometric_key(mesh.vertex_coordinates(key), precision): key for key in mesh.vertices()}
    for xyz in points:
        gkey = geometric_key(xyz, precision)
        if gkey in gkey_key:
            key = gkey_key[gkey]
            keys.append(key)
    return keys
