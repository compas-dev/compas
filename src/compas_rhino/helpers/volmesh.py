from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas

from compas.utilities import geometric_key

from compas_rhino.artists import VolMeshArtist

from compas_rhino.selectors import VertexSelector
from compas_rhino.selectors import EdgeSelector
from compas_rhino.selectors import FaceSelector

try:
    import Rhino
    import scriptcontext as sc

except ImportError:
    compas.raise_if_ironpython()


__author__    = ['Tom Van Mele']
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'volmesh_from_polysurfaces',
    'volmesh_from_wireframe',

    'volmesh_draw',
    'volmesh_draw_vertices',
    'volmesh_draw_edges',
    'volmesh_draw_faces',
    'volmesh_draw_cells',

    'volmesh_select_vertex',
    'volmesh_select_vertices',
    'volmesh_select_edge',
    'volmesh_select_edges',
    'volmesh_select_face',
    'volmesh_select_faces',
]


def volmesh_from_polysurfaces(cls, guids):
    """Construct a volumetric mesh from given polysurfaces.

    Essentially, this function does the following:

    * find each of the polysurfaces and check if they have a boundary representation (b-rep)
    * convert to b-rep and extract the edge loops
    * make a face of each loop by referring to vertices using their geometric keys
    * add a cell per brep
    * and add the faces of a brep to the cell
    * create a volmesh from the found vertices and cells

    Parameters:
        cls (compas.datastructures.volmesh.VolMesh):
            The class of volmesh.
        guids (sequence of str or System.Guid):
            The *globally unique identifiers* of the polysurfaces.

    Returns:
        compas.datastructures.volmesh.Volmesh: The volumetric mesh object.

    """
    gkey_xyz = {}
    cells = []

    for guid in guids:
        cell = []
        obj = sc.doc.Objects.Find(guid)

        if not obj.Geometry.HasBrepForm:
            continue

        brep = Rhino.Geometry.Brep.TryConvertBrep(obj.Geometry)

        for loop in brep.Loops:
            curve = loop.To3dCurve()
            segments = curve.Explode()
            face = []
            sp = segments[0].PointAtStart
            ep = segments[0].PointAtEnd
            sp_gkey = geometric_key(sp)
            ep_gkey = geometric_key(ep)
            gkey_xyz[sp_gkey] = sp
            gkey_xyz[ep_gkey] = ep
            face.append(sp_gkey)
            face.append(ep_gkey)
            for segment in segments[1:-1]:
                ep = segment.PointAtEnd
                ep_gkey = geometric_key(ep)
                face.append(ep_gkey)
                gkey_xyz[ep_gkey] = ep
            cell.append(face)
        cells.append(cell)

    gkey_index = dict((gkey, index) for index, gkey in enumerate(gkey_xyz))
    vertices   = [list(xyz) for gkey, xyz in gkey_xyz.items()]
    cells      = [[[gkey_index[gkey] for gkey in face] for face in cell] for cell in cells]

    return cls.from_vertices_and_cells(vertices, cells)


def volmesh_from_wireframe(cls, edges):
    raise NotImplementedError


# ==============================================================================
# drawing
# ==============================================================================


def volmesh_draw(volmesh,
                 layer=None,
                 clear_layer=False,
                 vertexcolor=None,
                 edgecolor=None,
                 facecolor=None):
    """Draw a volmesh.

    Parameters
    ----------
    volmesh : compas.datastructures.VolMesh
        A volmesh object.
    layer : str (None)
        The layer to draw in.
        Default is to draw in the current layer.
    clear_layer : bool (False)
        Clear the current layer.
    vertexcolor : str, tuple, list, dict (None)
        The vertex color specification.
        Default is to use the color of the parent layer.
    edgecolor : str, tuple, list, dict (None)
        The edge color specification.
        Default is to use the color of the parent layer.
    facecolor : str, tuple, list, dict (None)
        The face color specification.
        Default is to use the color of the parent layer.

    Examples
    --------
    >>> volmesh_draw(volmesh)
    >>> volmesh_draw(volmesh, layer='SomeLayer')
    >>> volmesh_draw(volmesh, clear_layer=True)
    >>> volmesh_draw(volmesh, vertexcolor='#ff0000')
    >>> volmesh_draw(volmesh, edgecolor=(0, 255, 0))
    >>> volmesh_draw(volmesh, facecolor={key: (0.0, 0.0, 0.5) for key in volmesh.faces()})

    See Also
    --------
    * compas_rhino.VolMeshArtist

    """
    artist = VolMeshArtist(volmesh)
    artist.layer = layer
    if clear_layer:
        artist.clear_layer()
    artist.clear()
    artist.draw_vertices(color=vertexcolor)
    artist.draw_edges(color=edgecolor)
    artist.draw_faces(color=facecolor)
    artist.redraw()


def volmesh_draw_vertices(volmesh,
                          keys=None,
                          color=None,
                          layer=None,
                          clear_layer=False,
                          redraw=True):
    """Draw the vertices of a volmesh.

    Parameters
    ----------
    volmesh : compas.datastructures.VolMesh
        A volmesh object.
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
    layer : str (None)
        The layer in which the vertices are drawn.
        Default is to draw in the current layer.
    clear_layer : bool (False)
        Clear the drawing layer.
    redraw : bool (True)
        Redraw the view after adding the vertices.

    Examples
    --------
    >>> volmesh_draw_vertices(volmesh)
    >>> volmesh_draw_vertices(volmesh, keys=volmesh.vertices_on_boundary())
    >>> volmesh_draw_vertices(volmesh, color='#00ff00')
    >>> color = {key: (('#ff0000') if volmesh.vertex_is_on_boundary(key) else ('#00ff00')) for key in volmesh.vertices()}
    >>> volmesh_draw_vertices(volmesh, color=color)

    See Also
    --------
    * compas_rhino.VolMeshArtist

    """
    artist = VolMeshArtist(volmesh)
    artist.layer = layer
    if clear_layer:
        artist.clear_layer()
    artist.clear_vertices()
    artist.draw_vertices(color=color)
    if redraw:
        artist.redraw()


def volmesh_draw_edges(volmesh,
                       keys=None,
                       color=None,
                       layer=None,
                       clear_layer=False,
                       redraw=True):
    """Draw the edges of a volmesh.

    Parameters
    ----------
    volmesh : compas.datastructures.VolMesh
        A volmesh object.
    keys : list (None)
        A list of edge keys identifying which edges to draw.
        Default is to draw all edges.
    color : str, tuple, dict (None)
        The color specififcation for the edges.
        Colors should be specified in the form of a string (hex colors) or as a tuple of RGB components.
        To apply the same color to all edges, provide a single color specification.
        Individual colors can be assigned using a dictionary of key-color pairs.
        Missing keys will be assigned the default vertex color (``self.defaults['vertex.color']``).
        Default is use the color of the parent layer.
    layer : str (None)
        The layer in which the edges are drawn.
        Default is to draw in the current layer.
    clear_layer : bool (False)
        Clear the drawing layer.
    redraw : bool (True)
        Redraw the view after adding the edges.

    Examples
    --------
    >>> volmesh_draw_edges(volmesh)
    >>> volmesh_draw_edges(volmesh, keys=volmesh.edges_on_boundary())
    >>> volmesh_draw_edges(volmesh, color='#00ff00')
    >>> color = {key: (('#ff0000') if volmesh.vertex_is_on_boundary(key) else ('#00ff00')) for key in volmesh.edges()}
    >>> volmesh_draw_edges(volmesh, color=color)

    See Also
    --------
    * compas_rhino.VolMeshArtist

    """
    artist = VolMeshArtist(volmesh)
    artist.layer = layer
    if clear_layer:
        artist.clear_layer()
    artist.clear_edges()
    artist.draw_edges(color=color)
    if redraw:
        artist.redraw()


def volmesh_draw_faces(volmesh,
                       keys=None,
                       color=None,
                       layer=None,
                       clear_layer=False,
                       redraw=True):
    """Draw the faces of a volmesh.

    Parameters
    ----------
    volmesh : compas.datastructures.VolMesh
        A volmesh object.
    keys : list (None)
        A list of edge keys identifying which faces to draw.
        Default is to draw all faces.
    color : str, tuple, dict (None)
        The color specififcation for the faces.
        Colors should be specified in the form of a string (hex colors) or as a tuple of RGB components.
        To apply the same color to all faces, provide a single color specification.
        Individual colors can be assigned using a dictionary of key-color pairs.
        Missing keys will be assigned the default vertex color (``self.defaults['vertex.color']``).
        Default is use the color of the parent layer.
    layer : str (None)
        The layer in which the faces are drawn.
        Default is to draw in the current layer.
    clear_layer : bool (False)
        Clear the drawing layer.
    redraw : bool (True)
        Redraw the view after adding the faces.

    Examples
    --------
    >>> volmesh_draw_faces(volmesh)
    >>> volmesh_draw_faces(volmesh, keys=volmesh.faces_on_boundary())
    >>> volmesh_draw_faces(volmesh, color='#00ff00')
    >>> color = {key: (('#ff0000') if volmesh.vertex_is_on_boundary(key) else ('#00ff00')) for key in volmesh.faces()}
    >>> volmesh_draw_faces(volmesh, color=color)

    See Also
    --------
    * compas_rhino.VolMeshArtist

    """
    artist = VolMeshArtist(volmesh)
    artist.layer = layer
    if clear_layer:
        artist.clear_layer()
    artist.clear_faces()
    artist.draw_faces(color=color)
    if redraw:
        artist.redraw()


def volmesh_draw_cells(volmesh):
    pass


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


# ==============================================================================
# modifications
# ==============================================================================


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures import VolMesh
    from compas_rhino import volmesh_draw
    from compas_rhino import volmesh_select_vertex
    # from compas_rhino import volmesh_move_vertex

    volmesh = VolMesh.from_obj(compas.get('boxes.obj'))

    volmesh_draw(volmesh, layer='test', clear_layer=True)

    key = volmesh_select_vertex(volmesh)

    print(key)

    # if volmesh_move_vertex(volmesh, key):
    #     volmesh_draw(volmesh, layer='test', clear_layer=True)
