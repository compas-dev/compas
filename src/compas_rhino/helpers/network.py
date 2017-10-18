from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import ast

from compas.utilities import color_to_colordict
from compas.utilities import geometric_key
from compas.geometry import distance_point_point

import compas_rhino

from compas_rhino.helpers.artists.networkartist import NetworkArtist
from compas_rhino.helpers.modifiers.networkmodifier import NetworkModifier

from compas_rhino.helpers.selectors import VertexSelector
from compas_rhino.helpers.selectors import EdgeSelector
from compas_rhino.helpers.selectors import FaceSelector


__author__    = 'Tom Van Mele'
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'network_draw',
    'network_draw_vertices',
    'network_draw_edges',
    'network_select_vertices',
    'network_select_vertex',
    'network_select_edges',
    'network_select_edge',
    'network_select_faces',
    'network_select_face',
    'network_update_attributes',
    'network_update_vertex_attributes',
    'network_update_from_points',
    'network_update_edge_attributes',
    'network_update_from_lines',
    'network_update_face_attributes',
    'network_display_vertex_labels',
    'network_display_edge_labels',
    'network_display_face_labels',
    'network_move',
    'network_move_vertex',
    'network_display_axial_forces',
    'network_display_reaction_forces',
    'network_display_residual_forces',
    'network_display_selfweight',
    'network_display_applied_loads',
]


# ==============================================================================
# constructors
# ==============================================================================

# ==============================================================================
# artists
# ==============================================================================

def network_draw(network,
                 layer=None,
                 clear_layer=False,
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
    * network_draw_vertices
    * network_draw_edges

    Example
    -------
    .. code-block:: python

        import compas
        from compas.datastructures import Network
        import compas_rhino as compas_rhino

        network = Network.from_obj(compas.get_data('lines.obj'))

        compas_rhino.network_draw(network)

    """
    artist = NetworkArtist(network)
    artist.layer = layer

    if clear_layer:
        artist.clear_layer()

    artist.clear()
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
    ``"{}.vertex.{}".format(self.network.attributes['name'], key)``.
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
    ``"{}.edge.{}-{}".fromat(self.network.attributes['name'], u, v)``.
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


# ==============================================================================
# select
# ==============================================================================


def network_select_vertices(network, message="Select network vertices."):
    """Select vertices of a network.

    Parameters:
        network (compas.datastructures.network.Network): The network object.
        message (str): Optional. The message to display to the user.
            Default is ``"Select network vertices."``

    Returns:
        list: The keys of the selected vertices.

    Note:
        Selection is based on naming conventions.
        When a network is drawn using the function :func:`network_draw`,
        the point objects representing the vertices get assigned a name that
        has the following pattern::

            '{0}.vertex.{1}'.format(network.attributes['name'], key)

    Example:

        .. code-block:: python
            :emphasize-lines: 9

            from compas.datastructures.network import Network
            import compas_rhino as compas_rhino as rhino

            guids = compas_rhino.select_objects()
            lines = compas_rhino.select_line_coordinates(guids)

            network = Network.from_lines(lines)

            keys = compas_rhino.network_select_vertices(network)

            print(keys)


    See Also:
        * :func:`network_select_edges`
        * :func:`network_select_faces`

    """
    return VertexSelector.select_vertices(network)


def network_select_vertex(network, message="Select a network vertex"):
    """Select one vertex of a network.

    Parameters:
        network (compas.datastructures.network.Network): The network object.
        message (str): Optional. The message to display to the user.
            Default is ``"Select network vertex."``

    Returns:
        * str: The key of the selected vertex.
        * None: If no vertex was selected.

    See Also:
        * :func:`network_select_vertices`

    """
    return VertexSelector.select_vertex(network)


def network_select_edges(network, message="Select network edges"):
    """Select edges of a network.

    Parameters:
        network (compas.datastructures.network.Network): The network object.
        message (str): Optional. The message to display to the user.
            Default is ``"Select network edges."``

    Returns:
        list: The keys of the selected edges. Each key is a *uv* pair.

    Note:
        Selection is based on naming conventions.
        When a network is drawn using the function :func:`network_draw`,
        the curve objects representing the edges get assigned a name that
        has the following pattern::

            '{0}.edge.{1}-{2}'.format(network.attributes['name'], u, v)

    See Also:
        * :func:`network_select_vertices`
        * :func:`network_select_faces`

    """
    return EdgeSelector.select_edges(network)


def network_select_edge(network, message="Select a network edge"):
    """Select one edge of a network.

    Parameters:
        network (compas.datastructures.network.Network): The network object.
        message (str): Optional. The message to display to the user.
            Default is ``"Select network edges."``

    Returns:
        tuple: The key of the selected edge.
        None: If no edge was selected.

    See Also:
        * :func:`network_select_edges`

    """
    return EdgeSelector.select_edge(network)


def network_select_faces(network, message='Select network faces.'):
    """Select faces of a network.

    Parameters:
        network (compas.datastructures.network.Network): The network object.
        message (str): Optional. The message to display to the user.
            Default is ``"Select network edges."``

    Returns:
        list: The keys of the selected faces.

    Note:
        Selection of faces is based on naming conventions.
        When a network is drawn using the function :func:`network_draw`,
        the curve objects representing the edges get assigned a name that
        has the following pattern::

            '{0}.edge.{1}-{2}'.format(network.attributes['name'], u, v)

    Example:

        .. code-block:: python
            :emphasize-lines: 14

            import compas
            from compas.datastructures.network import Network
            from compas.datastructures.network.algorithms import find_network_faces

            import compas_rhino as compas_rhino as rhino

            network = Network.from_obj(compas.get_data('lines.obj'))

            find_network_faces(network, network.leaves())

            compas_rhino.network_draw(network)
            compas_rhino.network_display_face_labels(network)

            fkeys = compas_rhino.network_select_faces(network)

            print(fkeys)


    See Also:
        * :func:`network_select_vertices`
        * :func:`network_select_edges`

    """
    return FaceSelector.select_faces(network)


def network_select_face(network, message='Select face.'):
    """Select one face of a network.

    Parameters:
        network (compas.datastructures.network.Network): The network object.
        message (str): Optional. The message to display to the user.
            Default is ``"Select network edges."``

    Returns:
        tuple: The key of the selected face.
        None: If no face was selected.

    See Also:
        * :func:`network_select_faces`

    """
    return FaceSelector.select_face(network)


# ==============================================================================
# attributes
# ==============================================================================


def network_update_attributes(network):
    """Update the attributes of a network.

    Parameters:
        network (compas.datastructures.network.Network): The network object.

    Returns:
        bool: ``True`` if the update was successful, and ``False`` otherwise.

    Example:

        .. code-block:: python

            import compas
            import compas_rhino as compas_rhino
            from compas.datastructures.network import Network

            network = Network.from_obj(compas.get_data('lines.obj'))

            if compas_rhino.network_update_attributes(network):
                print('network attributes updated')
            else:
                print('network attributres not updated')


    See Also:
        * :func:`network_update_vertex_attributes`
        * :func:`network_update_edge_attributes`
        * :func:`network_update_face_attributes`

    """
    names  = sorted(network.attributes.keys())
    values = [str(network.attributes[name]) for name in names]
    values = compas_rhino.update_named_values(names, values)
    if values:
        for name, value in zip(names, values):
            try:
                network.attributes[name] = ast.literal_eval(value)
            except (ValueError, TypeError):
                network.attributes[name] = value
        return True
    return False


def network_update_vertex_attributes(network, keys, names=None):
    """Update the attributes of the vertices of a network.

    Parameters:
        network (compas.datastructures.network.Network): The network object.
        keys (tuple, list): The keys of the vertices to update.
        names (tuple, list): Optional. The names of the atrtibutes to update.
            Defaults to ``None``. If ``None``, all attributes are included in the
            update.

    Returns:
        bool: ``True`` if the update was successful, and ``False`` otherwise.

    Example:

        .. code-block:: python

            import compas
            import compas_rhino as compas_rhino

            from compas.datastructures.network import Network

            network = Network.from_obj(compas.get_data('lines.obj'))

            keys = network.vertices()

            if compas_rhino.network_update_vertex_attributes(network, keys):
                print('network vertex attributes updated')
            else:
                print('network vertex attributes not updated')


    See Also:
        * :func:`network_update_attributes`
        * :func:`network_update_edge_attributes`
        * :func:`network_update_face_attributes`

    """
    if not names:
        names = network.default_vertex_attributes.keys()
    names = sorted(names)
    values = [network.vertex[keys[0]][name] for name in names]
    if len(keys) > 1:
        for i, name in enumerate(names):
            for key in keys[1:]:
                if values[i] != network.vertex[key][name]:
                    values[i] = '-'
                    break
    values = map(str, values)
    values = compas_rhino.update_named_values(names, values)
    if values:
        for name, value in zip(names, values):
            if value != '-':
                for key in keys:
                    try:
                        network.vertex[key][name] = ast.literal_eval(value)
                    except (ValueError, TypeError):
                        network.vertex[key][name] = value
        return True
    return False


def network_update_from_points(network, guids):
    points = compas_rhino.get_point_coordinates(guids)
    names = compas_rhino.get_object_names(guids)
    gkey_key = {geometric_key(network.vertex_coordinates(key)): key for key in network}
    for i, xyz in enumerate(points):
        name = names[i]
        try:
            attr = ast.literal_eval(name)
        except ValueError:
            pass
        else:
            gkey = geometric_key(xyz)
            if gkey in gkey_key:
                key = gkey_key[gkey]
                network.vertex[key].update(attr)


def network_update_edge_attributes(network, keys, names=None):
    """Update the attributes of the edges of a network.

    Parameters:
        network (compas.datastructures.network.Network): The network object.
        keys (tuple, list): The keys of the edges to update. Note that the keys
            should be pairs of vertex keys.
        names (tuple, list): Optional. The names of the atrtibutes to update.
            Defaults to ``None``. If ``None``, all attributes are included in the
            update.

    Returns:
        bool: ``True`` if the update was successful, and ``False`` otherwise.

    Example:

        .. code-block:: python

            import compas
            import compas_rhino as compas_rhino

            from compas.datastructures.network import Network

            network = Network.from_obj(compas.get_data('lines.obj'))

            keys = network.edges()

            if compas_rhino.network_update_edge_attributes(network, keys):
                print('network edge attributes updated')
            else:
                print('network edge attributes not updated')


    See Also:
        * :func:`network_update_attributes`
        * :func:`network_update_vertex_attributes`
        * :func:`network_update_face_attributes`

    """
    if not names:
        names = network.default_edge_attributes.keys()
    names = sorted(names)
    u, v = keys[0]
    values = [network.edge[u][v][name] for name in names]
    if len(keys) > 1:
        for i, name in enumerate(names):
            for u, v in keys[1:]:
                if values[i] != network.edge[u][v][name]:
                    values[i] = '-'
                    break
    values = map(str, values)
    values = compas_rhino.update_named_values(names, values)
    if values:
        for name, value in zip(names, values):
            if value != '-':
                for u, v in keys:
                    try:
                        network.edge[u][v][name] = ast.literal_eval(value)
                    except (ValueError, TypeError):
                        network.edge[u][v][name] = value
        return True
    return False


def network_update_from_lines(network, guids):
    lines = compas_rhino.get_line_coordinates(guids)
    names = compas_rhino.get_object_names(guids)
    gkey_key = {geometric_key(network.vertex_coordinates(key)): key for key in network}
    for i, (sp, ep) in enumerate(lines):
        name = names[i]
        try:
            attr = ast.literal_eval(name)
        except ValueError:
            pass
        else:
            a = geometric_key(sp)
            b = geometric_key(ep)
            if a in gkey_key and b in gkey_key:
                u = gkey_key[a]
                v = gkey_key[b]
                if v in network.edge[u]:
                    network.edge[u][v].update(attr)
                else:
                    network.edge[v][u].update(attr)


def network_update_face_attributes(network, fkeys, names=None):
    """Update the attributes of the faces of a network.

    Parameters:
        network (compas.datastructures.network.Network): The network object.
        keys (tuple, list): The keys of the faces to update.
        names (tuple, list): Optional. The names of the atrtibutes to update.
            Defaults to ``None``. If ``None``, all attributes are included in the
            update.

    Returns:
        bool: ``True`` if the update was successful, and ``False`` otherwise.

    Example:

        .. code-block:: python

            import compas
            import compas_rhino as compas_rhino

            from compas.datastructures.network import Network

            network = Network.from_obj(compas.get_data('lines.obj'))

            keys = network.faces()

            if compas_rhino.network_update_face_attributes(network, keys):
                print('network face attributes updated')
            else:
                print('network face attributes not updated')


    See Also:
        * :func:`network_update_attributes`
        * :func:`network_update_vertex_attributes`
        * :func:`network_update_edge_attributes`

    """
    if not network.dualdata:
        return
    if not names:
        names = sorted(network.default_face_attributes.keys())
    values = [network.dualdata.vertex[fkeys[0]][name] for name in names]
    if len(fkeys) > 1:
        for i, name in enumerate(names):
            for fkey in fkeys[1:]:
                if values[i] != network.dualdata.vertex[fkey][name]:
                    values[i] = '-'
                    break
    values = map(str, values)
    values = compas_rhino.update_attributes(names, values)
    if values:
        for name, value in zip(names, values):
            if value != '-':
                for fkey in fkeys:
                    try:
                        network.dualdata.vertex[fkey][name] = ast.literal_eval(value)
                    except (ValueError, TypeError):
                        network.dualdata.vertex[fkey][name] = value
        return True
    return False


# ==============================================================================
# labels
# ==============================================================================

# use color callables to generate dynamic colors
# rename formatter to data_formatter

def network_display_vertex_labels(network, attr_name=None, layer=None, color=None, formatter=None):
    """Display labels for the vertices of a network.

    Parameters:
        network (compas.datastructures.network.Network): The network object.
        attr_name (str): Optional. The name of the attribute value to display in the label.
            Default is ``None``. If ``None``, the key of the vertex is displayed.
        layer (str): Optional. The layer to draw in. Default is ``None``.
        color (str, tuple, list, dict): Optional. The color specification. Default is ``None``.
            The following values are supported:

                * str: A HEX color. For example, ``'#ff0000'``.
                * tuple, list: RGB color. For example, ``(255, 0, 0)``.
                * dict: A dictionary of RGB and/or HEX colors.

            If ``None``, the default vertex color of the network will be used.
        formatter (callable): Optional. A formatting function. Default is ``None``.

    Example:

        .. code-block:: python

            import compas
            import compas_rhino as compas_rhino

            from compas.datastructures.network import Network

            network = Network.from_obj(compas.get_data('lines.obj'))

            compas_rhino.network_display_vertex_labels(network)


        .. code-block:: python

            import compas
            import compas_rhino as compas_rhino

            from compas.datastructures.network import Network

            network = Network.from_obj(compas.get_data('lines.obj'))

            def formatter(value):
                return '{0:.3f}'.format(value)

            compas_rhino.network_display_vertex_labels(network, attr_name='x' formatter=formatter)


    See Also:
        * :func:`network_display_edge_labels`
        * :func:`network_display_face_labels`

    """
    if not attr_name:
        attr_name = 'key'

    if formatter:
        if not callable(formatter):
            raise Exception('The provided formatter is not callable.')
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
    artist.draw_vertexlabels(text=text)
    artist.redraw()


def network_display_edge_labels(network, attr_name=None, layer=None, color=None, formatter=None):
    """Display labels for the edges of a network.

    Parameters:
        network (compas.datastructures.network.Network): The network object.
        attr_name (str): Optional. The name of the attribute value to display in the label.
            Default is ``None``. If ``None``, the key of the edge is displayed.
        layer (str): Optional. The layer to draw in. Default is ``None``.
        color (str, tuple, list, dict): Optional. The color specification. Default is ``None``.
            The following values are supported:

                * str: A HEX color. For example, ``'#ff0000'``.
                * tuple, list: RGB color. For example, ``(255, 0, 0)``.
                * dict: A dictionary of RGB and/or HEX colors.

            If ``None``, the default edge color of the network will be used.
        formatter (callable): Optional. A formatting function. Default is ``None``.

    Example:

        .. code-block:: python

            import compas
            import compas_rhino as compas_rhino

            from compas.datastructures.network import Network

            network = Network.from_obj(compas.get_data('lines.obj'))

            compas_rhino.network_display_edge_labels(network)


    See Also:
        * :func:`network_display_vertex_labels`
        * :func:`network_display_face_labels`

    """
    compas_rhino.delete_objects(compas_rhino.get_objects(name="{0}.edge.label.*".format(network.attributes['name'])))

    if not attr_name:
        attr_name = 'key'

    colordict = color_to_colordict(color,
                                   network.edges(),
                                   default=network.attributes['color.vertex'],
                                   colorformat='rgb',
                                   normalize=False)
    if formatter:
        if not callable(formatter):
            raise Exception('The provided formatter is not callable.')
    else:
        formatter = str

    labels = []

    for index, (u, v, attr) in enumerate(network.edges(True)):

        if attr_name == 'key':
            value = '{0}-{1}'.format(u, v)
        elif attr_name == 'index':
            value = index
        else:
            value = attr[attr_name]

        labels.append({'pos'  : network.edge_midpoint(u, v),
                       'text' : formatter(value),
                       'name' : '{0}.edge.label.{1}-{2}'.format(network.attributes['name'], u, v),
                       'color': colordict[(u, v)], })

    compas_rhino.xdraw_labels(
        labels,
        layer=layer,
        clear=False,
        redraw=True
    )


def network_display_face_labels(network, attr_name=None, layer=None, color=None, formatter=None):
    """Display labels for the faces of a network.

    Parameters:
        network (compas.datastructures.network.Network): The network object.
        attr_name (str): Optional. The name of the attribute value to display in the label.
            Default is ``None``. If ``None``, the key of the face is displayed.
        layer (str): Optional. The layer to draw in. Default is ``None``.
        color (str, tuple, list, dict): Optional. The color specification. Default is ``None``.
            The following values are supported:

                * str: A HEX color. For example, ``'#ff0000'``.
                * tuple, list: RGB color. For example, ``(255, 0, 0)``.
                * dict: A dictionary of RGB and/or HEX colors.

            If ``None``, the default face color of the network will be used.
        formatter (callable): Optional. A formatting function. Default is ``None``.

    Example:

        .. code-block:: python

            import compas
            import compas_rhino as compas_rhino

            from compas.datastructures.network import Network

            network = Network.from_obj(compas.get_data('lines.obj'))

            compas_rhino.network_display_face_labels(network)


    See Also:
        * :func:`network_display_vertex_labels`
        * :func:`network_display_edge_labels`

    """
    compas_rhino.delete_objects(compas_rhino.get_objects(name="{0}.face.label.*".format(network.attributes['name'])))

    if not attr_name:
        attr_name = 'key'

    colordict = color_to_colordict(color,
                                   network.faces(),
                                   default=network.attributes['color.face'],
                                   colorformat='rgb',
                                   normalize=False)

    if formatter:
        if not callable(formatter):
            raise Exception('The provided formatter is not callable.')
    else:
        formatter = str

    labels = []

    for index, fkey in enumerate(network.faces()):
        if attr_name == 'key':
            value = fkey
        elif attr_name == 'index':
            value = index
        else:
            value = network.facedata[fkey][attr_name]

        labels.append({
            'pos'  : network.face_centroid(fkey),
            'text' : formatter(value),
            'name' : '{0}.face.label.{1}'.format(network.attributes['name'], fkey),
            'color': colordict[fkey]
        })

    compas_rhino.xdraw_labels(
        labels,
        layer=layer,
        clear=False,
        redraw=True
    )


# ==============================================================================
# geometry
# ==============================================================================


def network_move(network):
    """Move the entire network.

    Parameters:
        network (compas.datastructures.network.Network): A network object.

    """
    return NetworkModifier.move(network)


def network_move_vertex(network, key, constraint=None, allow_off=None):
    """Move on vertex of the network.

    Parameters:
        network (compas.datastructures.network.Network): The network object.
        key (str): The vertex to move.
        constraint (Rhino.Geometry): Optional. A ``Rhino.Geometry`` object to
            constrain the movement to. Default is ``None``.
        allow_off (bool): Optional. Allow the vertex to move off the constraint.
            Default is ``None``.

    Example:

        .. code-block:: python

            import compas
            import compas_rhino as compas_rhino

            from compas.datastructures.network import Network

            network = Network.from_obj(compas.get_data('lines.obj'))

            key = compas_rhino.network_select_vertex(network)

            if key:
                compas_rhino.network_move_vertex(network, key)

    """
    return NetworkModifier.move_vertex(network, key, constraint=constraint, allow_off=allow_off)


# ==============================================================================
# forces
# ==============================================================================


def network_display_axial_forces(network,
                                 display=True,
                                 layer=None,
                                 clear_layer=False,
                                 scale=1.0,
                                 attr_name='f',
                                 color_tension=(255, 0, 0),
                                 color_compression=(0, 0, 255)):
    """Display the axial forces in the edges of a network.

    Parameters:
        network (compas.datastructures.network.Network):
            The network object.
        display (bool): Optional.
            If ``True``, display the axial forces.
            If ``False``, don't display the axial forces.
            Default is ``True``.
        layer (str): Optional.
            The layer to draw in. Default is ``None``.
        clear_layer (bool): Optional.
            Flag for clearing the layer.
            Default is ``False``.
        scale (float): Optional.
            The scale of the forces.
            Default is ``1.0``.
        attr_name (str): Optional.
            The name of the edge attribute storing the force value.
            Default is ``'f'``.
        color_tension (tuple): Optional.
            The color to use for tension forces.
            Default is ``(255, 0, 0)``.
        color_compression (tuple): Optional.
            The color to use for compression forces.
            Default is ``(0, 0, 255)``.

    Example:

        .. code-block:: python

            import random
            import compas
            import compas_rhino as compas_rhino

            from compas.datastructures.network import Network

            network = Network.from_obj(compas.get_data('lines.obj'))

            for u, v, attr in network.edges(True):
                attr['f'] = random.choice([-1.0, 1.0]) * random.randint(1, 10)

            compas_rhino.network_display_axial_forces(network)

    See Also:
        * :func:`network_display_reaction_forces`
        * :func:`network_display_residual_forces`
        * :func:`network_display_selfweight`

    """
    tol = compas_rhino.get_tolerance()
    objects = compas_rhino.get_objects(name='{0}.force:axial.*'.format(network.attributes['name']))
    compas_rhino.delete_objects(objects)

    if not display:
        return

    lines = []

    for u, v, attr in network.edges(True):
        start  = network.vertex_coordinates(u)
        end    = network.vertex_coordinates(v)
        force  = attr['f']
        color  = color_tension if force > 0.0 else color_compression
        radius = scale * ((force ** 2) ** 0.5 / 3.14159) ** 0.5
        name   = '{0}.force:axial.{1}-{2}'.format(network.attributes['name'], u, v)

        if radius < tol:
            continue

        lines.append({
            'start' : start,
            'end'   : end,
            'name'  : name,
            'color' : color,
            'radius': radius,
        })

    compas_rhino.xdraw_cylinders(lines, layer=layer, clear=clear_layer)


def network_display_reaction_forces(network,
                                    display=True,
                                    layer=None,
                                    clear_layer=False,
                                    scale=1.0,
                                    color=(0, 255, 0),
                                    attr_name='is_anchor'):

    tol = compas_rhino.get_tolerance()
    objects = compas_rhino.get_objects(name='{0}.force:reaction.*'.format(network.attributes['name']))
    compas_rhino.delete_objects(objects)

    if not display:
        return

    lines = []

    for key, attr in network.vertices(True):

        if not attr[attr_name]:
            continue

        force  = attr['rx'], attr['ry'], attr['rz']
        start  = network.vertex_coordinates(key)
        end    = [start[i] - scale * force[i] for i in range(3)]
        length = sum((end[i] - start[i]) ** 2 for i in range(3)) ** 0.5
        arrow  = 'end'
        name   = '{0}.force:reaction.{1}'.format(network.attributes['name'], key)

        if length < tol:
            continue

        lines.append({
            'start': start,
            'end'  : end,
            'name' : name,
            'color': color,
            'arrow': arrow,
        })

    compas_rhino.xdraw_lines(lines, layer=layer, clear=clear_layer)


def network_display_residual_forces(network,
                                    display=True,
                                    layer=None,
                                    clear_layer=False,
                                    scale=1.0,
                                    color=(0, 255, 255),
                                    attr_name='is_anchor'):

    tol = compas_rhino.get_tolerance()
    guids = compas_rhino.get_objects(name='{0}.force:residual.*'.format(network.attributes['name']))
    compas_rhino.delete_objects(guids)

    if not display:
        return

    lines = []

    for key, attr in network.vertices(True):

        if attr[attr_name]:
            continue

        force  = attr['rx'], attr['ry'], attr['rz']
        start  = network.vertex_coordinates(key)
        end    = [start[i] + scale * force[i] for i in range(3)]
        length = distance_point_point(start, end)
        arrow  = 'end'
        name   = '{0}.force:residual.{1}'.format(network.attributes['name'], key)

        if length < tol:
            continue

        lines.append({
            'start' : start,
            'end'   : end,
            'name'  : name,
            'color' : color,
            'arrow' : arrow,
        })

    compas_rhino.xdraw_lines(lines, layer=layer, clear=clear_layer)


def network_display_selfweight(network,
                               display=True,
                               layer=None,
                               clear_layer=False,
                               scale=1.0,
                               color=(0, 255, 0)):

    tol = compas_rhino.get_tolerance()
    guids = compas_rhino.get_objects(name='{0}.force:selfweight.*'.format(network.attributes['name']))
    compas_rhino.delete_objects(guids)

    if not display:
        return

    lines = []

    for key, attr in network.vertices(True):
        load   = 0, 0, network.vertex_area(key)
        start  = network.vertex_coordinates(key)
        end    = [start[i] - scale * load[i] for i in range(3)]
        name   = '{0}.force:selfweight.{1}'.format(network.attributes['name'], key)
        arrow  = 'end'
        length = distance_point_point(start, end)

        if length < tol:
            continue

        lines.append({
            'start': start,
            'end'  : end,
            'name' : name,
            'color': color,
            'arrow': arrow,
        })

    compas_rhino.xdraw_lines(lines, layer=layer, clear=clear_layer)


def network_display_applied_loads(network,
                                  display=True,
                                  layer=None,
                                  clear_layer=False,
                                  scale=1.0,
                                  color=(0, 0, 255)):

    tol = compas_rhino.get_tolerance()
    guids = compas_rhino.get_objects(name='{0}.force:load.*'.format(network.attributes['name']))
    compas_rhino.delete_objects(guids)

    if not display:
        return

    lines = []

    for key, attr in network.vertices(True):
        load   = attr['px'], attr['py'], attr['pz']
        end    = network.vertex_coordinates(key)
        start  = [end[i] - scale * load[i] for i in range(3)]
        length = distance_point_point(start, end)
        arrow  = 'end'
        name   = '{0}.force:load.{1}'.format(network.attributes['name'], key)

        if length < tol:
            continue

        lines.append({
            'start': start,
            'end'  : end,
            'name' : name,
            'color': color,
            'arrow': arrow,
        })

    compas_rhino.xdraw_lines(lines, layer=layer, clear=clear_layer)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures import Network
    from compas_rhino.helpers import network_draw
    from compas_rhino.helpers import network_select_vertex
    from compas_rhino.helpers import network_move_vertex

    network = Network.from_obj(compas.get_data('lines.obj'))

    network_draw(network, layer='test', clear_layer=True)

    key = network_select_vertex(network)

    if network_move_vertex(network, key):
        network_draw(network, layer='test', clear_layer=True)
