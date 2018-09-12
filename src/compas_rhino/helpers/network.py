from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas_rhino.artists import NetworkArtist

from compas_rhino.modifiers import Modifier
from compas_rhino.modifiers import VertexModifier
from compas_rhino.modifiers import EdgeModifier

from compas_rhino.selectors import VertexSelector
from compas_rhino.selectors import EdgeSelector


__all__ = [
    'network_draw',
    'network_draw_vertices',
    'network_draw_edges',
    'network_draw_vertex_labels',
    'network_draw_edge_labels',

    'network_select_vertices',
    'network_select_vertex',
    'network_select_edges',
    'network_select_edge',

    'network_update_attributes',
    'network_update_vertex_attributes',
    'network_update_edge_attributes',

    'network_move',
    'network_move_vertex',

    'network_draw_reaction_forces',
    'network_draw_loads',
    'network_draw_axial_forces'
]


# def network_update_from_points(network, guids):
#     points = compas_rhino.get_point_coordinates(guids)
#     names = compas_rhino.get_object_names(guids)
#     gkey_key = {geometric_key(network.vertex_coordinates(key)): key for key in network}
#     for i, xyz in enumerate(points):
#         name = names[i]
#         try:
#             attr = ast.literal_eval(name)
#         except ValueError:
#             pass
#         else:
#             gkey = geometric_key(xyz)
#             if gkey in gkey_key:
#                 key = gkey_key[gkey]
#                 network.vertex[key].update(attr)


# def network_update_from_lines(network, guids):
#     lines = compas_rhino.get_line_coordinates(guids)
#     names = compas_rhino.get_object_names(guids)
#     gkey_key = {geometric_key(network.vertex_coordinates(key)): key for key in network}
#     for i, (sp, ep) in enumerate(lines):
#         name = names[i]
#         try:
#             attr = ast.literal_eval(name)
#         except ValueError:
#             pass
#         else:
#             a = geometric_key(sp)
#             b = geometric_key(ep)
#             if a in gkey_key and b in gkey_key:
#                 u = gkey_key[a]
#                 v = gkey_key[b]
#                 if v in network.edge[u]:
#                     network.edge[u][v].update(attr)
#                 else:
#                     network.edge[v][u].update(attr)


# ==============================================================================
# drawing
# ==============================================================================


def network_draw(network,
                 layer=None,
                 clear_layer=False,
                 clear_vertices=True,
                 clear_edges=True,
                 vertexcolor=None,
                 edgecolor=None):
    """Draw a network data structure in Rhino.

    Parameters
    ----------
    network : compas.datastructures.Network
        A network object.
    layer : str (None)
        The layer to draw in.
        Default is the current layer.
    clear_layer : bool (False)
        Clear the layer.
    vertexcolor : list, tuple, str, dict (None)
        The color specification for the vertices.
        * list, tuple: rgb color, with color specs between 0 and 255 (e.g. ``(255, 0, 0)``).
        * str: hex color (e.g. ``'#ff0000'``).
        * dict: dictionary of hex or rgb colors.
    edgecolor : list, tuple, str, dict (None)
        The color specification for the edges.
        * list, tuple: rgb color, with color specs between 0 and 255 (e.g. ``(255, 0, 0)``).
        * str: hex color (e.g. ``'#ff0000'``).
        * dict: dictionary of hex or rgb color.

    Notes
    -----
    * Any network objects with the same name that are already present in the
      model will be deleted by this function.
    * To also clear the entire layer the network will be drawn on, for
      example, if you have a dedicated network layer, use the ``clear_layer`` flag as well.

    See Also
    --------
    * :func:`network_draw_vertices`
    * :func:`network_draw_edges`

    Examples
    --------
    >>>

    """
    artist = NetworkArtist(network)
    artist.layer = layer

    if clear_layer:
        artist.clear_layer()

    if clear_vertices:
        artist.clear_vertices()

    if clear_edges:
        artist.clear_edges()

    artist.draw_vertices(color=vertexcolor)
    artist.draw_edges(color=edgecolor)
    artist.redraw()


def network_draw_vertices(network,
                          keys=None,
                          color=None,
                          layer=None,
                          clear_layer=False,
                          redraw=True):
    """Draw a selection of vertices of a network.

    Parameters
    ----------
    keys : list (None)
        A list of vertex keys identifying which vertices to draw.
        Default is to draw all vertices.
    color : str, tuple, dict (None)
        The color specififcation for the vertices.
        Colors should be specified in the form of a string (hex colors) or as a tuple of RGB components.
        To apply the same color to all vertices, provide a single color specification.
        Individual colors can be assigned using a dictionary of key-color pairs.
        Missing keys will be assigned the default vertex color (``self.defaults['color.vertex']``).
        Default is to inherit the color from the layer.
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
    ``"{}.vertex.{}".format(self.network.name, key)``.
    This name is used afterwards to identify vertices of the networkin the Rhino model.

    Examples
    --------
    >>> network_draw_vertices(network)
    >>> network_draw_vertices(network, color='#ff0000')
    >>> network_draw_vertices(network, color=(255, 0, 0))
    >>> network_draw_vertices(network, keys=network.vertices_on_boundary())
    >>> network_draw_vertices(network, color={(u, v): '#00ff00' for u, v in network.vertices_on_boundary()})

    """
    artist = NetworkArtist(network)
    artist.layer = layer
    if clear_layer:
        artist.clear_layer()
    artist.clear_vertices()
    artist.draw_vertices(keys=keys, color=color)
    if redraw:
        artist.redraw()


def network_draw_edges(network,
                       keys=None,
                       color=None,
                       layer=None,
                       clear_layer=False,
                       redraw=True):
    """Draw a selection of edges of the network.

    Parameters
    ----------
    keys : list (None)
        A list of edge keys (as uv pairs) identifying which edges to draw.
        Default is to draw all edges.
    color : str, tuple, dict (None)
        The color specififcation for the edges.
        Colors should be specified in the form of a string (hex colors) or as a tuple of RGB components.
        To apply the same color to all faces, provide a single color specification.
        Individual colors can be assigned using a dictionary of key-color pairs.
        Missing keys will be assigned the default face color (``self.defaults['face.color']``).
        Default is to inherit color from the parent layer.
    layer : str (None)
        The layer in which the vertices are drawn.
        Default is to draw in the current layer.
    clear_layer : bool (False)
        Clear the drawing layer.
    redraw : bool (True)
        Redraw the view after adding the vertices.

    Notes
    -----
    All edges are named using the following template:
    ``"{}.edge.{}-{}".fromat(self.network.name, u, v)``.
    This name is used afterwards to identify edges of the network in the Rhino model.

    Examples
    --------
    >>> network_draw_edges(network)
    >>> network_draw_edges(network, color='#ff0000')
    >>> network_draw_edges(network, color=(255, 0, 0))
    >>> network_draw_edges(network, keys=network.edges_xxx())
    >>> network_draw_edges(network, color={(u, v): '#00ff00' for u, v in network.edges_xxx()})

    """
    artist = NetworkArtist(network)
    artist.layer = layer
    if clear_layer:
        artist.clear_layer()
    artist.clear_edges()
    artist.draw_edges(keys=keys, color=color)
    if redraw:
        artist.redraw()


def network_draw_vertex_labels(network,
                               attr_name=None,
                               layer=None,
                               color=None,
                               formatter=None):
    """Draw labels for the vertices of the network.

    Parameters
    ----------
    network : compas.datastructures.Network
        A network object.
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
    ``"{}.vertex.label.{}".format(self.network.name, key)``.
    This name is used afterwards to identify vertices of the networkin the Rhino model.

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
    for index, (key, attr) in enumerate(network.vertices(True)):
        if 'key' == attr_name:
            value = key
        elif 'index' == attr_name:
            value = index
        else:
            value = attr[attr_name]
        text[key] = formatter(value)

    artist = NetworkArtist(network)
    artist.layer = layer
    artist.clear_vertexlabels()
    artist.draw_vertexlabels(text=text, color=color)
    artist.redraw()


def network_draw_edge_labels(network,
                             text=None,
                             layer=None,
                             color=None):
    """Draw labels for the edges of a network.

    Parameters
    ----------
    network : compas.datastructures.Network
        A network object.
    text : str (None)
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
    ``"{}.edge.label.{}".format(self.network.name, key)``.
    This name is used afterwards to identify edges of the network in the Rhino model.

    Examples
    --------
    >>>

    """

    # if formatter:
    #     assert callable(formatter), 'The provided formatter is not callable.'
    # else:
    #     formatter = str

    if not text or text == 'key':
        text = {(u, v): '{}-{}'.format(u, v) for u, v in network.edges()}
    elif text == 'index':
        text = {(u, v): str(index) for index, (u, v) in enumerate(network.edges())}
    else:
        pass

    artist = NetworkArtist(network)
    artist.layer = layer
    artist.clear_edgelabels()
    artist.draw_edgelabels(text=text, color=color)
    artist.redraw()


# ==============================================================================
# selections
# ==============================================================================


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


# ==============================================================================
# modifications
# ==============================================================================


def network_move(network):
    """Move the entire network.

    Parameters
    ----------
    network : compas.datastructures.Network
        A network object.

    See Also
    --------
    * :func:`network_move_vertex`

    """
    return Modifier.move(network)


def network_update_attributes(network):
    """Update the attributes of a network.

    Parameters
    ----------
    network : compas.datastructures.Network
        A network object.

    Returns
    -------
    bool
        ``True`` if the update was successful.
        ``False`` otherwise.

    See Also
    --------
    * :func:`network_update_vertex_attributes`
    * :func:`network_update_edge_attributes`

    """
    return Modifier.update_attributes(network)


def network_move_vertex(network, key, constraint=None, allow_off=False):
    """Move on vertex of the network.

    Parameters
    ----------
    network : compas.datastructures.Network
        A network object.
    key : str
        The vertex to move.
    constraint : Rhino.Geometry (None)
        A Rhino geometry object to constrain the movement to.
        By default the movement is unconstrained.
    allow_off : bool (False)
        Allow the vertex to move off the constraint.

    """
    return VertexModifier.move_vertex(network, key, constraint=constraint, allow_off=allow_off)


def network_update_vertex_attributes(network, keys, names=None):
    """Update the attributes of the vertices of a network.

    Parameters
    ----------
    network : compas.datastructures.Network
        A network object.
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
    * :func:`network_update_attributes`
    * :func:`network_update_edge_attributes`

    """
    return VertexModifier.update_vertex_attributes(network, keys, names=names)


def network_update_edge_attributes(network, keys, names=None):
    """Update the attributes of the edges of a network.

    Parameters
    ----------
    network : compas.datastructures.Network
        A network object.
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
    * :func:`network_update_attributes`
    * :func:`network_update_vertex_attributes`

    """
    return EdgeModifier.update_edge_attributes(network, keys, names=names)


# ==============================================================================
# temp
# ==============================================================================


def network_draw_reaction_forces(network, scale=1.0, layer=None, clear_layer=False):
    lines = []
    for key, attr in network.vertices(True):
        if attr['is_fixed']:
            force = attr['rx'], attr['ry'], attr['rz']
            start = network.vertex_coordinates(key)
            end = [start[axis] - scale * force[axis] for axis in (0, 1, 2)]
            lines.append({
                'start': start,
                'end'  : end,
                'name' : '{}.reaction.{}'.format(network.name, key),
                'color': (0, 255, 0),
                'arrow': 'end',
            })
    guids = compas_rhino.get_objects(name='{}.reaction.*'.format(network.name))
    compas_rhino.delete_objects(guids)
    compas_rhino.xdraw_lines(lines, layer=layer, clear=clear_layer)


def network_draw_loads(network, scale=1.0, layer=None, clear_layer=False):
    lines = []
    for key, attr in network.vertices(True):
        if not attr['is_fixed']:
            force = attr['px'], attr['py'], attr['pz']
            start = network.vertex_coordinates(key)
            end = [start[axis] + scale * force[axis] for axis in (0, 1, 2)]
            lines.append({
                'start': start,
                'end'  : end,
                'name' : '{}.load.{}'.format(network.name, key),
                'color': (0, 255, 255),
                'arrow': 'end',
            })
    guids = compas_rhino.get_objects(name='{}.load.*'.format(network.name))
    compas_rhino.delete_objects(guids)
    compas_rhino.xdraw_lines(lines, layer=layer, clear=clear_layer)


def network_draw_axial_forces(network, scale=0.1, layer=None, clear_layer=False):
    cylinders = []
    for u, v, attr in network.edges(True):
        if attr['f'] > 0.0:
            cylinders.append({
                'start' : network.vertex_coordinates(u),
                'end'   : network.vertex_coordinates(v),
                'radius': scale * 3.14159 * attr['f'] ** 2,
                'name'  : '{}.axial.{}-{}'.format(network.name, u, v),
                'color' : (255, 0, 0),
            })
    guids = compas_rhino.get_objects(name='{}.axial.*'.format(network.name))
    compas_rhino.delete_objects(guids)
    compas_rhino.xdraw_cylinders(cylinders, layer=layer, clear=clear_layer)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures import Network
    from compas_rhino import network_draw
    from compas_rhino import network_select_vertex
    from compas_rhino import network_move_vertex

    network = Network.from_obj(compas.get('lines.obj'))

    network_draw(network, layer='test', clear_layer=True)

    key = network_select_vertex(network)

    if network_move_vertex(network, key):
        network_draw(network, layer='test', clear_layer=True)
