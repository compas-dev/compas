from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_ghpython.artists import MeshArtist


__all__ = [
    'mesh_draw',
    'mesh_draw_vertices',
    'mesh_draw_edges',
    'mesh_draw_faces',
]


def mesh_draw(mesh, color=None):
    """
    Draw a mesh object in Rhino.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        The mesh object.
    color : str, tuple, list, dict (None)
        The vertex color specification.
        Defaults to None.

    Notes
    -----
    Colors can be specifiedin different ways:

    * str: A hexadecimal color that will be applied to all elements subject to the specification.
    * tuple, list: RGB color that will be applied to all elements subject to the specification.
    * dict: RGB or hex color dict with a specification for some or all of the related elements.

    Notes
    -----
    RGB colors specified as values between 0 and 255, should be integers.
    RGB colors specified as values between 0.0 and 1.0, should be floats.
    """

    artist = MeshArtist(mesh)
    return artist.draw(color)


def mesh_draw_vertices(mesh,
                       keys=None,
                       color=None):
    """Draw a selection of vertices of the mesh.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        A mesh object.
    keys : list (None)
        A list of vertex keys identifying which vertices to draw.
        Default is to draw all vertices.
    color : str, tuple, dict (None)
        The color specififcation for the vertices.
        Colors should be specified in the form of a string (hex colors) or as a tuple of RGB components.
        To apply the same color to all vertices, provide a single color specification.
        Individual colors can be assigned using a dictionary of key-color pairs.
        Missing keys will be assigned the default vertex color (``self.defaults['vertex.color']``).
        Default is use the color of the parent layer.

    Notes
    -----
    The vertices are named using the following template:
    ``"{}.vertex.{}".format(self.mesh.attributes['name'], key)``.
    This name is used afterwards to identify vertices of the meshin the Rhino model.

    Examples
    --------
    >>>

    """
    artist = MeshArtist(mesh)
    return artist.draw_vertices(keys, color)


def mesh_draw_edges(mesh,
                    keys=None,
                    color=None):
    """Draw a selection of edges of the mesh.

    Parameters
    ----------
    keys : list
        A list of edge keys (as uv pairs) identifying which edges to draw.
        Default is to draw all edges.

    Notes
    -----
    All edges are named using the following template:
    ``"{}.edge.{}-{}".fromat(self.mesh.attributes['name'], u, v)``.

    Examples
    --------
    >>> mesh_draw_edges(mesh)
    >>> mesh_draw_edges(mesh, keys=mesh.edges_on_boundary())

    """
    artist = MeshArtist(mesh)
    return artist.draw_edges(keys, color)


def mesh_draw_faces(mesh,
                    keys=None,
                    color=None,
                    join_faces=False):
    """Draw a selection of faces of the mesh.

    Parameters
    ----------
    keys : list (None)
        A list of face keys identifying which faces to draw.
        Default is to draw all faces.
    join_faces : bool (False)
        Join the faces into a polymesh object.

    Notes
    -----
    The faces are named using the following template:
    ``"{}.face.{}".format(self.mesh.attributes['name'], key)``.

    Examples
    --------
    >>>

    """
    artist = MeshArtist(mesh)
    return artist.draw_faces(keys, color, join_faces)
