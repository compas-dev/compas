from __future__ import print_function

import compas
import compas_rhino

from compas.utilities import geometric_key

from compas_rhino.geometry import RhinoSurface

from compas_rhino.artists import MeshArtist

from compas_rhino.modifiers import Modifier
from compas_rhino.modifiers import VertexModifier
from compas_rhino.modifiers import EdgeModifier
from compas_rhino.modifiers import FaceModifier

from compas_rhino.selectors import VertexSelector
from compas_rhino.selectors import EdgeSelector
from compas_rhino.selectors import FaceSelector

try:
    import Rhino
    import scriptcontext as sc
    import rhinoscriptsyntax as rs

except ImportError:
    compas.raise_if_ironpython()


__author__    = ['Tom Van Mele']
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'mesh_from_guid',
    'mesh_from_surface',
    'mesh_from_surface_uv',
    'mesh_from_surface_heightfield',

    'mesh_draw',
    'mesh_draw_vertices',
    'mesh_draw_edges',
    'mesh_draw_faces',
    'mesh_draw_vertex_labels',
    'mesh_draw_edge_labels',
    'mesh_draw_face_labels',

    'mesh_select_vertices',
    'mesh_select_vertex',
    'mesh_select_edges',
    'mesh_select_edge',
    'mesh_select_faces',
    'mesh_select_face',

    'mesh_update_vertex_attributes',
    'mesh_update_edge_attributes',
    'mesh_update_face_attributes',
    'mesh_move_vertex',
    'mesh_identify_vertices',
]


# ==============================================================================
# constructors
# ==============================================================================


def mesh_from_guid(cls, guid):
    """Construct a mesh from a Rhino mesh.

    Parameters
    ----------
    cls : Mesh
        A mesh type.
    guid : str
        The GUID of the Rhino mesh.

    Returns
    -------
    Mesh
        A mesh object.

    """
    vertices, faces = compas_rhino.get_mesh_vertices_and_faces(guid)
    faces = [face[:-1] if face[-2] == face[-1] else face for face in faces]
    mesh  = cls.from_vertices_and_faces(vertices, faces)
    return mesh


def mesh_from_surface(cls, guid):
    """Construct a mesh from a Rhino surface.

    Parameters
    ----------
    cls : Mesh
        A mesh type.
    guid : str
        The GUID of the Rhino surface.

    Returns
    -------
    Mesh
        A mesh object.

    """
    gkey_xyz = {}
    faces = []
    obj = sc.doc.Objects.Find(guid)

    if not obj.Geometry.HasBrepForm:
        return

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

        faces.append(face)

    gkey_index = {gkey: index for index, gkey in enumerate(gkey_xyz)}
    vertices = [list(xyz) for gkey, xyz in gkey_xyz.items()]
    faces = [[gkey_index[gkey] for gkey in f] for f in faces]
    mesh = cls.from_vertices_and_faces(vertices, faces)

    return mesh


def mesh_from_surface_uv(cls, guid, density=(10, 10)):
    """Construct a mesh from a point cloud aligned with the uv space of a Rhino NURBS surface.

    Parameters
    ----------
    cls : Mesh
        The mesh type.
    guid : str
        The GUID of the surface.
    density : tuple
        The density of the point grid in the u and v directions.

    Returns
    -------
    Mesh
        A mesh object.

    See Also
    --------
    * :class:`compas_rhino.geometry.RhinoSurface`

    Examples
    --------
    >>>

    """
    return mesh_from_surface_heightfield(cls, guid, density=density)


def mesh_from_surface_heightfield(cls, guid, density=(10, 10)):
    """Create a mesh data structure from a point grid aligned with the uv space of a Rhino NURBS surface.

    Parameters
    ----------
    cls : Mesh
        The mesh type.
    guid : str
        The GUID of the surface.
    density : tuple
        The density of the point grid in the u and v directions.

    Returns
    -------
    Mesh
        A mesh object.

    See Also
    --------
    * :class:`compas_rhino.geometry.RhinoSurface`

    Examples
    --------
    >>>

    """
    try:
        u, v = density
    except Exception:
        u, v = density, density

    surface = RhinoSurface(guid)

    mesh = cls()

    vertices = surface.heightfield(density=(u, v), over_space=True)

    for x, y, z in vertices:
        mesh.add_vertex(x=x, y=y, z=z)

    for i in range(u - 1):
        for j in range(v - 1):
            face = ((i + 0) * v + j,
                    (i + 0) * v + j + 1,
                    (i + 1) * v + j + 1,
                    (i + 1) * v + j)
            mesh.add_face(face)

    return mesh


# ==============================================================================
# drawing
# ==============================================================================

def mesh_draw(mesh,
              layer=None,
              clear_layer=False,
              clear_vertices=False,
              clear_faces=False,
              clear_edges=False,
              show_faces=True,
              show_vertices=False,
              show_edges=False,
              vertexcolor=None,
              edgecolor=None,
              facecolor=None):
    """
    Draw a mesh object in Rhino.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        The mesh object.
    layer : str (None)
        The layer to draw in.
        Default is to draw in the current layer.
    clear_layer : bool (False)
        Clear the drawing layer.
    show_faces : bool (True)
        Draw the faces.
    show_vertices : bool (False)
        Draw the vertices.
    show_edges : bool (False)
        Draw the edges.
    vertexcolor : str, tuple, list, dict (None)
        The vertex color specification.
        Default is to use the color of the parent layer.
    edgecolor : str, tuple, list, dict (None)
        The edge color specification.
        Default is to use the color of the parent layer.
    facecolor : str, tuple, list, dict (None)
        The face color specification.
        Default is to use the color of the parent layer.

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
    artist.layer = layer

    if clear_layer:
        artist.clear_layer()

    if clear_vertices:
        artist.clear_vertices()
    if clear_edges:
        artist.clear_edges()
    if clear_faces:
        artist.clear_faces()

    if show_faces:
        artist.draw_faces(color=facecolor)
    if show_edges:
        artist.draw_edges(color=edgecolor)
    if show_vertices:
        artist.draw_vertices(color=vertexcolor)

    artist.redraw()


def mesh_draw_vertices(mesh,
                       keys=None,
                       color=None,
                       layer=None,
                       clear_layer=False,
                       clear_vertices=False,
                       redraw=True):
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
    layer : str (None)
        The layer in which the vertices are drawn.
        Default is to draw in the current layer.
    clear_layer : bool (False)
        Clear the drawing layer.
    redraw : bool (True)
        Redraw the view after adding the vertices.

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
    artist.layer = layer

    if clear_layer:
        artist.clear_layer()

    if clear_vertices:
        artist.clear_vertices()

    guids = artist.draw_vertices(color=color)

    if redraw:
        artist.redraw()

    return guids


def mesh_draw_edges(mesh,
                    keys=None,
                    color=None,
                    layer=None,
                    clear_layer=False,
                    redraw=True):
    """Draw a selection of edges of the mesh.

    Parameters
    ----------
    keys : list
        A list of edge keys (as uv pairs) identifying which edges to draw.
        Default is to draw all edges.
    color : str, tuple, dict
        The color specififcation for the edges.
        Colors should be specified in the form of a string (hex colors) or as a tuple of RGB components.
        To apply the same color to all faces, provide a single color specification.
        Individual colors can be assigned using a dictionary of key-color pairs.
        Missing keys will be assigned the default face color (``self.defaults['face.color']``).
        Default is use the color of the parent layer.
    layer : str (None)
        The layer in which the edges are drawn.
        Default is to draw in the current layer.
    clear_layer : bool (False)
        Clear the drawing layer.
    redraw : bool (True)
        Redraw the view after adding the edges.

    Notes
    -----
    All edges are named using the following template:
    ``"{}.edge.{}-{}".fromat(self.mesh.attributes['name'], u, v)``.
    This name is used afterwards to identify edges of the mesh in the Rhino model.

    Examples
    --------
    >>> mesh_draw_edges(mesh)
    >>> mesh_draw_edges(mesh, color='#ff0000')
    >>> mesh_draw_edges(mesh, color=(255, 0, 0))
    >>> mesh_draw_edges(mesh, keys=mesh.edges_on_boundary())
    >>> mesh_draw_edges(mesh, color={(u, v): '#00ff00' for u, v in mesh.edges_on_boundary()})

    """
    artist = MeshArtist(mesh)
    artist.layer = layer

    if clear_layer:
        artist.clear_layer()

    artist.clear_edges()
    guids = artist.draw_edges(color=color)

    if redraw:
        artist.redraw()

    return guids


def mesh_draw_faces(mesh,
                    keys=None,
                    color=None,
                    layer=None,
                    clear_layer=False,
                    clear_faces=False,
                    redraw=True,
                    join_faces=False):
    """Draw a selection of faces of the mesh.

    Parameters
    ----------
    keys : list (None)
        A list of face keys identifying which faces to draw.
        Default is to draw all faces.
    color : str, tuple, dict (None)
        The color specififcation for the faces.
        Colors should be specified in the form of a string (hex colors) or as a tuple of RGB components.
        To apply the same color to all faces, provide a single color specification.
        Individual colors can be assigned using a dictionary of key-color pairs.
        Missing keys will be assigned the default face color (``self.defaults['face.color']``).
        Default is to use the color of the parent layer.
    layer : str (None)
        The layer in which the edges are drawn.
        Default is to draw in the current layer.
    clear_layer : bool (False)
        Clear the drawing layer.
    redraw : bool (True)
        Redraw the view after adding the edges.
    join_faces : bool (False)
        Join the faces into a polymesh object.

    Notes
    -----
    The faces are named using the following template:
    ``"{}.face.{}".format(self.mesh.attributes['name'], key)``.
    This name is used afterwards to identify faces of the mesh in the Rhino model.

    Examples
    --------
    >>>

    """
    artist = MeshArtist(mesh)
    artist.layer = layer

    if clear_layer:
        artist.clear_layer()

    if clear_faces:
        artist.clear_faces()
    
    guids = artist.draw_faces(color=color)

    if redraw:
        artist.redraw()

    if join_faces:
        guid = rs.JoinMeshes(guids, delete_input=True)
        return guid

    return guids


def mesh_draw_vertex_labels(mesh,
                            attr_name=None,
                            layer=None,
                            color=None,
                            formatter=None):
    """Draw labels for the vertices of a mesh.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        A mesh object.
    attr_name : str (None)
        The name of the attribute value to display in the label.
        Default is is to display the vertex key.
    layer : str (None)
        The layer to draw in.
        Default is to draw in the current layer.
    color : str, tuple, list, dict (None)
        The color specififcation for the labels.
        Colors should be specified in the form of a string (hex colors) or as a tuple of RGB components.
        To apply the same color to all face labels, provide a single color specification.
        Individual colors can be assigned using a dictionary of key-color pairs.
        Missing keys will be assigned the default vertex color (``self.defaults['vertex.color']``).
        Default is to inherit color from the parent layer.
    formatter : callable (None)
        A formatting function.
        Defaults to the built-in ``str`` function.

    Notes
    -----
    The labels are named using the following template:
    ``"{}.vertex.label.{}".format(self.mesh.name, key)``.
    This name is used afterwards to identify vertices of the meshin the Rhino model.

    Examples
    --------
    >>>

    """
    if not attr_name:
        attr_name = 'key'

    if formatter:
        assert callable(formatter), 'The provided formatter is not callable.'
    else:
        formatter = str

    text = {}
    for index, (key, attr) in enumerate(mesh.vertices(True)):
        if 'key' == attr_name:
            value = key
        elif 'index' == attr_name:
            value = index
        else:
            value = attr[attr_name]
        text[key] = formatter(value)

    artist = MeshArtist(mesh)
    artist.layer = layer
    artist.clear_vertexlabels()
    artist.draw_vertexlabels(text=text, color=color)
    artist.redraw()


def mesh_draw_edge_labels(mesh, attr_name=None, layer=None, color=None, formatter=None):
    """Display labels for the edges of a mesh.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        A mesh object.
    attr_name : str (None)
        The name of the attribute value to display in the label.
        Default is to display the edge keys.
    layer : str (None)
        The layer to draw in.
        Default is to draw in the current layer.
    color : str, tuple, list, dict (None)
        The color specififcation for the labels.
        Colors should be specified in the form of a string (hex colors) or as a tuple of RGB components.
        To apply the same color to all face labels, provide a single color specification.
        Individual colors can be assigned using a dictionary of key-color pairs.
        Missing keys will be assigned the default edge color (``self.defaults['edge.color']``).
        Default is to inherit color from the parent layer.
    formatter : callable (None)
        A formatting function.
        Defaults to the built-in ``str`` function.

    Notes
    -----
    The labels are named using the following template:
    ``"{}.edge.label.{}".format(self.mesh.name, key)``.
    This name is used afterwards to identify edges of the mesh in the Rhino model.

    Examples
    --------
    >>>

    """

    if not attr_name:
        attr_name = 'key'

    if formatter:
        assert callable(formatter), 'The provided formatter is not callable.'
    else:
        formatter = str

    text = {}
    for index, (u, v, attr) in enumerate(mesh.vertices(True)):
        if 'key' == attr_name:
            value = '{}-{}'.format(u, v)
        elif 'index' == attr_name:
            value = index
        else:
            value = attr[attr_name]
        text[(u, v)] = formatter(value)

    artist = MeshArtist(mesh)
    artist.layer = layer
    artist.clear_edgelabels()
    artist.draw_edgelabels(text=text, color=color)
    artist.redraw()


def mesh_draw_face_labels(mesh,
                          attr_name=None,
                          layer=None,
                          color=None,
                          formatter=None):
    """Display labels for the faces of a mesh.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        A mesh object.
    attr_name : str (None)
        The name of the attribute value to display in the label.
        Default is is to display the face key.
    layer : str (None)
        The layer to draw in.
        Default is to draw in the current layer.
    color : str, tuple, list, dict (None)
        The color specififcation for the labels.
        Colors should be specified in the form of a string (hex colors) or as a tuple of RGB components.
        To apply the same color to all face labels, provide a single color specification.
        Individual colors can be assigned using a dictionary of key-color pairs.
        Missing keys will be assigned the default face color (``self.defaults['face.color']``).
        Default is to inherit color from the parent layer.
    formatter : callable (None)
        A formatting function.
        Defaults to the built-in ``str`` function.

    Notes
    -----
    The labels are named using the following template:
    ``"{}.face.label.{}".format(self.mesh.name, key)``.
    This name is used afterwards to identify faces of the meshin the Rhino model.

    Examples
    --------
    >>>

    """
    if not attr_name:
        attr_name = 'key'

    if formatter:
        assert callable(formatter), 'The provided formatter is not callable.'
    else:
        formatter = str

    text = {}
    for index, (key, attr) in enumerate(mesh.faces(True)):
        if 'key' == attr_name:
            value = key
        elif 'index' == attr_name:
            value = index
        else:
            value = attr[attr_name]
        text[key] = formatter(value)

    artist = MeshArtist(mesh)
    artist.layer = layer
    artist.clear_facelabels()
    artist.draw_facelabels(text=text, color=color)
    artist.redraw()


# def mesh_draw_vertex_normals(mesh,
#                              display=True,
#                              layer=None,
#                              scale=1.0,
#                              color=(0, 0, 255)):
#     """"""
#     guids = compas_rhino.get_objects(name='{0}.vertex.normal.*'.format(mesh.attributes['name']))
#     compas_rhino.delete_objects(guids)

#     if not display:
#         return

#     lines = []

#     for key in mesh.vertices():
#         normal = mesh.vertex_normal(key)
#         start  = mesh.vertex_coordinates(key)
#         end    = [start[axis] + normal[axis] for axis in range(3)]
#         name   = '{0}.vertex.normal.{1}'.format(mesh.attributes['name'], key)

#         lines.append({
#             'start': start,
#             'end'  : end,
#             'name' : name,
#             'color': color,
#             'arrow': 'end',
#         })

#     compas_rhino.xdraw_lines(lines, layer=layer, clear=False, redraw=True)


# def mesh_draw_face_normals(mesh,
#                            display=True,
#                            layer=None,
#                            scale=1.0,
#                            color=(0, 0, 255)):
#     """"""
#     guids = compas_rhino.get_objects(name='{0}.face.normal.*'.format(mesh.attributes['name']))
#     compas_rhino.delete_objects(guids)

#     if not display:
#         return

#     lines = []

#     for fkey in mesh.faces():
#         normal = mesh.face_normal(fkey)
#         start  = mesh.face_center(fkey)
#         end    = [start[axis] + normal[axis] for axis in range(3)]
#         name   = '{0}.face.normal.{1}'.format(mesh.attributes['name'], fkey)

#         lines.append({
#             'start' : start,
#             'end'   : end,
#             'name'  : name,
#             'color' : color,
#             'arrow' : 'end',
#         })

#     compas_rhino.xdraw_lines(lines, layer=layer, clear=False, redraw=True)


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


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures import Mesh
    from compas_rhino import mesh_draw
    from compas_rhino import mesh_select_vertex
    from compas_rhino import mesh_move_vertex

    mesh = Mesh.from_obj(compas.get_data('quadmesh_planar.obj'))

    mesh_draw(mesh, layer='test', clear_layer=True)
